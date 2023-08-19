#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import os
import datetime

import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, angular_separation, get_sun
from astropy.table import Table

from scipy.spatial import KDTree

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


from astropy.utils.iers import conf
conf.auto_max_age = None



def weight_times(x):
    xg = [0,   5.0, 10.0, 20.0,  50.0,   1000.0]
    yg = [0.0, 0.1,  1.0,  1.0,   0.3,      0.0]
    return np.interp(x, xg, yg)

def weight_rel_point_dist(x):
    xg = [0.0, 9.0, 10.0, 11.0,  30.0,]
    yg = [0.0, 0.1,  1.0,  0.1,   0.0]
    return np.interp(x, xg, yg)



# def calc_travel_time(pts_azel_to, pt_azel_from):
#     X = np.abs(pts_azel_to[:,0] - pt_azel_from[0])
#     Y = np.abs(pts_azel_to[:,1] - pt_azel_from[1])
#     coeff = np.array([ 4.24341322e+00,  5.19835700e-01,  6.90580613e-01, -2.45717536e-03,
#         7.68404024e-04, -2.07442561e-05,  3.99111826e-03,  1.08131914e-03,
#        -5.49453808e-02])
#     return np.sum([c*prt for c, prt in zip(coeff, [X*0+1, X, Y, X**2, X**2*Y, X**2*Y**2, Y**2, X*Y**2, X*Y])], axis=0)

def calc_travel_time(pts_azel_to, pt_azel_from, v_az=3.0, v_el=1.35, b_az=3., b_el=6.):
    dt_az = (np.abs(pts_azel_to[:,0] - pt_azel_from[0]) / v_az) + b_az
    dt_el = (np.abs(pts_azel_to[:,1] - pt_azel_from[1]) / v_el) + b_el
    return np.max(np.column_stack([dt_az, dt_el]), axis=1)


def calc_ang_dist(xy1, xy2):
    xy1, xy2 = np.deg2rad(xy1), np.deg2rad(xy2)
    d = np.array([angular_separation(xy1[:,0], xy1[:,1], xy2[i,0], xy2[i,1]) for i in range(len(xy2))])
    return np.rad2deg(d)


def plot_azel(xy, t=None):

    x, y = xy[:,0], xy[:,1]
    x[x > 180] -= 360

    fig, ax1 = plt.subplots(figsize=(10,4))
    ax1.scatter(x, y)

    fig, ax2 = plt.subplots(subplot_kw=dict(projection="polar"))
    ax2.set_rlim(bottom=90, top=0)
    ax2.scatter(np.deg2rad(x), y)


class ObservationScheduler:
    def __init__(self, loc, T_script_start, 
        pt_start = (0, 90), 
        dt_track=100, 
        el_range=(21, 85), 
        az_range=(-270, 270), 
        mag_range = (2.5, 5),
        targetfile='hipparcos.vot', dt_start_wait_hr=2.,
        weight_balance =  0.35,
        random_offset = 0.1,
        compensate_proper_motion = True
        ) -> None:

        if isinstance(T_script_start, str):
            T_script_start = Time(T_script_start.replace('T', ' '), format='iso')
        elif isinstance(T_script_start, datetime.datetime):
            T_script_start = Time(T_script_start)

        self.pt_start = list(pt_start)

        self.pts_hist = []
        self.names_hist = []
        self.times_hist = []
        
        self.last_dc = None
        self.last_pts_poss = None
        self.last_score = None
        self.last_i = None
        
        self.weight_balance = weight_balance
        self.random_offset = random_offset

        self.T_script_start = T_script_start
        self.T_start_p = None
        self.T_end_p = None
        self.T_stop = None
        
        self.vot = None
        self.kptargets = None
        self.targetV = None

        self.az_range = az_range
        self.el_range = el_range
        self.mag_range = mag_range

        self.dt_track = dt_track

        self.loc = loc

        self.targetfile = targetfile
        self.compensate_proper_motion = compensate_proper_motion
        
        self.dt_start_wait = dt_start_wait_hr * u.hr

    @property
    def T_last(self):
        return Time(self.T_start_p) if len(self.times_hist) == 0 else self.times_hist[-1]

    @property
    def name_last(self):
        return None if len(self.names_hist) == 0 else self.names_hist[-1]

    @property
    def pt_last(self):
        return list(self.pt_start) if len(self.pts_hist) == 0 else self.pts_hist[-1]


    def stp_set_startstop(self, do_plot=False):
        T_noon = Time(self.T_script_start.datetime.replace(hour=12, minute=0, second=0), format='datetime')

        T_day = T_noon + np.linspace(0, 24*60, 24*60*5) * u.min
        sun = get_sun(T_day).transform_to(AltAz(obstime=T_day, location=self.loc))
        T_obs = T_day[sun.alt.deg < -18]

        self.T_start_p = np.min(T_obs) + self.dt_start_wait
        self.T_end_p = np.max(T_obs)
        self.T_stop = self.T_end_p - (200 + self.dt_track)*u.s

        if do_plot:
            plt.plot(T_day.datetime, sun.alt.deg)
            plt.axvline(self.T_start_p.datetime, color='k')
            plt.axvline(self.T_end_p.datetime, color='k')
            plt.axvline((self.T_start_p-self.dt_start_wait).datetime, color='k', linestyle='--')
            plt.axhline(-18, color='grey', linestyle='--')
            
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
            plt.xticks(rotation=90)

            # rotate and align the tick labels so they look better
            plt.gcf().autofmt_xdate()

    def stp_set_tables(self):
        
        file = ''
        if os.path.exists(self.targetfile):
            file = self.targetfile
        else:
            s = ['/home/jovyan/work/shared/hipparcos.vot', 
                 '/home/jovyan/shared/hipparcos.vot',
                r"D:\repos\mketests\(0) SARAO Test scripts repository\(1) InUse\Scheduling\hipparcos.vot"]
            s = [ss for ss in s if os.path.exists(ss)]
            if len(s) > 0: 
                file = s[0]
        
        self.vot = Table.read(file) #Read VOTable
        kptargets = self.vot.to_pandas() #Convert to pandas for compatibality with legacy script

        #Magnitude (brightness) filters
        mag_min, mag_max = self.mag_range
        
        #Get target details Hipparcos VOT table.
        vot = self.vot

        kptargets = kptargets[((kptargets['Vmag']<mag_max) & (kptargets['Vmag']>mag_min))]

        # hip_to_exclude = [95947, 74376, 74395, 34481, 27072, 54463, 2487, 14879, 114131, 13847, 30867, 2484, 122, 42568, 44659, 57803, 122, 57803]
        hip_to_exclude = [ 122, 154, 355, 1170, 2072, 2484, 2487, 13847, 14879, 17587, 27072, 27830, 30867, 34481, 42515, 42568, 44659, 54463, 57803, 66257, 70090, 70327, 73807, 74376, 74395, 74666, 80112, 95947, 98162, 107354, 110003, 112051, 112724, 114131]
        kptargets = kptargets[~np.isin(kptargets['HIP'], hip_to_exclude)]

        kptargets = kptargets.drop_duplicates(subset='HIP').sort_values(by='HIP')

        ra, dec = kptargets['_RAJ2000'].values * vot['_RAJ2000'].unit, kptargets['_DEJ2000'].values * vot['_DEJ2000'].unit
        pm_ra, pm_dec = kptargets['pmRA'].values * vot['pmRA'].unit, kptargets['pmDE'].values * vot['pmDE'].unit
        #Convert target into SkyCoord object
        targetV = SkyCoord(ra=ra, dec=dec, pm_ra_cosdec=pm_ra, pm_dec=pm_dec, obstime=Time('J2000'))

        if self.compensate_proper_motion:
            #Apply Proper Motion (Space motion without radial motion)
            tgtSM = targetV.apply_space_motion(new_obstime=Time.now()) #Time used to apply proper motion relative to obstime (J2000), not really needed to be this accurate
            targetV = SkyCoord(tgtSM.realize_frame(tgtSM.data.without_differentials())) #required to avoid UnitConversionError due radial velocit
        
        self.kptargets = kptargets
        self.targetV = SkyCoord(ra=kptargets['_RAJ2000']*u.deg, dec=kptargets['_DEJ2000']*u.deg, frame='icrs')


    def setup(self, do_plot = False):
        self.stp_set_startstop(do_plot)
        self.stp_set_tables()


    def get_dc_poss(self, T_0, dt_track=None, pt_now=None):
        
        
        if pt_now is None:
            pt_now = self.pt_last
            
        if dt_track is None:
            dt_track = self.dt_track
            
        assert self.targetV is not None, 'need to call setup() first '
        el_min, el_max = self.el_range
        az_min, az_max = self.az_range

        targetV = self.targetV
        loc = self.loc
        sname = self.kptargets['HIP']
        mag = self.kptargets['Vmag']

        
        # transform to local frame at start time
        tgt_altaz_T0 = targetV.transform_to(AltAz(location=loc, obstime=T_0))
        
        # filter by EL range
        idx = (tgt_altaz_T0.alt > el_min*u.deg) & (tgt_altaz_T0.alt < el_max*u.deg)    
        az0 = tgt_altaz_T0[idx].az.deg
        el0 = tgt_altaz_T0[idx].alt.deg
        names = sname.values[idx]
        mags = mag.values[idx]
        
        
        # get star positions in both directions (+AZ and -AZ)
        az0 = np.append(az0, az0-360)
        el0 = np.append(el0, el0)
        names = np.append(names, names)
        mags = np.append(mags, mags)
        
        # approximate dish travelling time and end time of tracking this star ( including travelling time )
        dt_travel = calc_travel_time(np.column_stack([az0, el0]), pt_now)
        T_1 = T_0 + (dt_track + dt_travel) * u.s
        
        # transform to local frame to determine approximate end position (both directions AZ+ and AZ-)
        n = len(tgt_altaz_T0[idx])
        tgt_altaz_T10 = targetV[idx].transform_to(AltAz(location=loc, obstime=T_1[:n]))
        tgt_altaz_T11 = targetV[idx].transform_to(AltAz(location=loc, obstime=T_1[n:]))
        
        # get approximate end positions (both directions AZ+ and AZ-)
        az1 = np.append(tgt_altaz_T10.az.deg, tgt_altaz_T11.az.deg-360)
        el1 = np.append(tgt_altaz_T10.alt.deg, tgt_altaz_T11.alt.deg)
        
        # filter by operation range
        idx = (az0 > az_min) & (az0 < az_max) 
        idx &= (az1 > az_min) & (az1 < az_max)
        idx &= (el0 > el_min) & (el0 < el_max)
        idx &= (el1 > el_min) & (el1 < el_max)
        
        # put output in dictionary
        return {
            'T_1': T_1[idx],
            'names': names[idx],
            'mags': mags[idx],
            'azel_0': np.column_stack([az0[idx], el0[idx]]),
            'azel_1': np.column_stack([az1[idx], el1[idx]]),
        } 
        
    def get_nearest_pt(self, T_0, pt_now, pt_cal):        
        dc_poss = self.get_dc_poss(T_0, dt_track=self.dt_track, pt_now=pt_now)
        
        pts_poss, names_poss = dc_poss['azel_0'], dc_poss['names']
        ang_dist, i_next = KDTree(pts_poss).query(pt_cal)
        
        name_next, pt_next, T_1 = names_poss[i_next], pts_poss[i_next, :], dc_poss['T_1'][i_next]
        return name_next, pt_next
    
    def get_reference_pt(self, T_0, pt_now):        
        dc_poss = self.get_dc_poss(T_0, dt_track=1, pt_now=pt_now)
        el_min, el_max = self.el_range
        az_min, az_max = self.az_range
        
        pts_poss, names_poss = dc_poss['azel_0'], dc_poss['names']
        
        pt = np.atleast_2d(np.array(pt_now))
        # get the angular distance between the current target point and all possible points
        # in order to find the best point for relative pointing
        ang_dists = np.min(calc_ang_dist(pt, pts_poss), axis=1)
        ang_dists_w = weight_rel_point_dist(ang_dists)
        i_ref = -1
        while i_ref < 0:
            i_ref = np.argmax(ang_dists_w)

            name_ref, pt_ref, T_1, ang_dist = names_poss[i_ref], pts_poss[i_ref, :], dc_poss['T_1'][i_ref], ang_dists[i_ref]

            dt = (T_1 - T_0).datetime.total_seconds()

            # clear out the 360° ambiguity
            d_az = pt_ref[0] - pt_now[0]
            if abs(d_az) > 180:
                pt_ref[0] -= np.sign(d_az) * 360
            if not ((az_min <= pt_ref[0] <= az_max) or (el_min <= pt_ref[1] <= el_max)):
                ang_dists_w[i_ref] = -np.inf
                i_ref = -1
                
                
        return name_ref, pt_ref, dt, ang_dist
        
    def tick(self, T_0, pt_now, dt_track=None, do_plot=True):
        pts_hist = self.pts_hist
            
        if dt_track is None:
            dt_track = self.dt_track
            
            
        dc_poss = self.get_dc_poss(T_0, dt_track=dt_track, pt_now=pt_now)
        pts_poss, names_poss = dc_poss['azel_0'], dc_poss['names']

        if len(pts_hist) == 0:
            # simply get the nearest possible star to starting position and select as first target
            ang_dist, i_next = KDTree(pts_poss).query(pt_now)
            score = None
        else:
            pts = np.atleast_2d(np.array(pts_hist))
            
            # get the angular distance between the history points and all possible points
            # in order to find areas which have not been covered properly yet
            ang_dist = np.min(calc_ang_dist(pts, pts_poss), axis=1)

            # any target over 30° angular distance away from any previously tracked target
            # qualifies as "best score"
            ang_dist[ang_dist > 30] = 30
            ang_dist_w = ang_dist / np.max(ang_dist) # normalize to 0...1
            
            # calc expected travelling times
            travel_time = calc_travel_time(pts_poss, pt_now)
            travel_time_w = weight_times(travel_time) # weight so that the results are 0...1
            
            # generate a score by balancing the two optimization criteria 
            # ( distance from nearest point previously tracked and travelling time to the point)
            score = ang_dist_w * self.weight_balance + travel_time_w * (1-self.weight_balance)
            # randomize results a little bit so that there is a bit of shuffling
            score += np.random.random(score.shape) * self.random_offset

            # get best possible target to track based on the score
            i_next = np.argmax(score)
        
        # get new point and associated info
        pt_next = pts_poss[i_next,:].tolist()
        name_next = names_poss[i_next]
        T_1 = dc_poss['T_1'][i_next]

        # add results to history and as current iter
        self.pts_hist.append(pt_next)
        self.names_hist.append(name_next)
        self.times_hist.append(T_1)
        self.last_pts_poss = pts_poss
        self.last_dc = dc_poss
        self.last_score = score
        self.last_i = i_next
        
        if do_plot and len(pts_hist) > 1:
            self.plot(dt_track)
            
        return name_next, pt_next
    
    def plot(self, dt_track=None):
        assert len(self.pts_hist) > 1, 'scheduler does not contain any data to plot!'

        T_1, T_0 = self.times_hist[-1], self.times_hist[-2]
        pt_next, pt_now = self.pts_hist[-1], self.pts_hist[-2] 
        pts = np.atleast_2d(np.array(self.pts_hist))
        pts_poss, score = self.last_pts_poss, self.last_score
        
        if dt_track is None:
            dt_track = self.dt_track
        
        dt = (T_1 - T_0).datetime.total_seconds() - dt_track

        d_ang = np.array(pt_next) - np.array(pt_now)
        f, ax = plt.subplots(1,1,figsize=(12,2))
        m = ax.scatter(pts_poss[:,0], pts_poss[:,1], s = 10, c=score)
        plt.colorbar(m)

        ax.plot(pts[:,0], pts[:,1], ' or', markersize=5)
        ax.plot(pts[-5:,0], pts[-5:,1], 'k')
        ax.plot([pt_now[0], pt_next[0]], [pt_now[1], pt_next[1]], 'k')
        ax.plot(pt_now[0], pt_now[1], ' om', markersize=7)
        ax.plot(pt_next[0], pt_next[1], ' ok', markersize=7)

        ax.set_title('T0: {} | PT: ({:.2f}°, {:.2f}°)\nd_ang: ({:.2f}°, {:.2f}°) | dt: {:.2f}sec'.format(T_0.datetime.isoformat(), pt_next[0], pt_next[1], d_ang[0], d_ang[1], dt))
        ax.axis('equal')
        
    def plot_dist(self):
        pts = np.atleast_2d(np.array(self.pts_hist))
        pt_now = self.pt_last
        x,y = pts[:,0], pts[:,1]
        fig, ax2 = plt.subplots(subplot_kw=dict(projection="polar"))
        ax2.set_rlim(bottom=90, top=0)
        ax2.scatter(np.deg2rad(x), y)
        ax2.plot(np.deg2rad(pt_now[0]), pt_now[1], ' xr', markersize=10)
        ax2.set_theta_zero_location("N")
        ax2.set_theta_direction(-1)
            
    def get_tracking_table(self, target, T_start, dt_track=None, pt_now = None, dt_grid=0.5):
        if dt_track is None:
            dt_track = self.dt_track
        if pt_now is None:
            pt_now = self.pt_last
            
        T = T_start + np.arange(0, dt_track, dt_grid) * u.s
        trgt = self.targetV[self.kptargets['HIP'] == target]
        altaz = trgt.transform_to(AltAz(location=self.loc, obstime=T))
        t, az, el = T.mjd, altaz.az.deg, altaz.alt.deg
        
        # make sure the track does not cross 360 deg
        az = np.unwrap(az, period=360)

        # if the track is closer the other way round offset az to negative degrees        
        if abs((az[0] - 360) - pt_now[0]) < abs(az[0] - pt_now[0]):
            az -= 360

        if abs((az[0] + 360) - pt_now[0]) < abs(az[0] - pt_now[0]):
            az += 360

        assert np.ptp(az) < 270, 'can not track a source where AZ changes by more than 270° over the course of tracking'
            
        return t, az, el
    


if __name__ == "__main__":


    dt_track=115
    el_range=(21, 80)
    az_range=(-180, 180)
    mag_range = (2.5, 5)
    dt_start_wait_hr=2.
    weight_balance =  0.35
    random_offset = 0.1

    my_antenna = {
                'address': '<ip-not-needed>',
                'altitude': 1086,
                'comments': 'Virtual simulator Antenna generated for testing',
                'configuration': 'test_antenna',
                'id': 's000',
                'lat': -30.7249,
                'lon': 21.45714,
                'params_json': '',
                'params_json_hist': '',
                'software_version': '001'
            }
    loc = EarthLocation(lat=my_antenna['lat'], lon=my_antenna['lon'], height=my_antenna['altitude']*u.m)  


    from mke_sculib.sim import scu_sim as scu_api


    antenna_ip = ''
    scu = scu_api(ip=antenna_ip, debug = False)


        
    start_condition = '2023-07-02T19:00:00Z'
    pt_now = pt_start = (0, 53)

    scheduler = ObservationScheduler(loc, start_condition, 
                                    pt_start = pt_start, dt_track=dt_track, el_range=el_range,
                                    az_range = az_range, mag_range=mag_range, dt_start_wait_hr=dt_start_wait_hr,
                                    weight_balance=weight_balance, random_offset=random_offset)



    scheduler.setup()
    scheduler.stp_set_startstop(do_plot=True)


    scu.move_to_azel(pt_start[0], pt_start[1])
    scu.wait_settle()

    T0 = scheduler.T_script_start + np.random.randint(-10, 10) * u.s

    print(T0, '...', scheduler.T_stop)

    while T0 < scheduler.T_stop:

        t0 = scu.t_internal

        name_next, pt_next = scheduler.tick(T0, pt_now = pt_now, do_plot=True)
        name_next, pt_next
        

        scu.move_to_azel(pt_next[0], pt_next[1])
        scu.wait_settle()

        t1 = scu.t_internal

        dt_exp = (scheduler.T_last - T0).to(u.s).value - scheduler.dt_track
        dt_real = (t1 - t0).to(u.s).value

        T0 += dt_real * u.s

        print('{: 10.0f} | HIP_{:06.0f} | [AZ={: 6.1f}°, EL={:2.1f}°] | dt_travel_exp={: 6.1f} sec | dt_travel_real={: 6.1f} sec | diff = {: 6.1f} sec'.format(len(scheduler.names_hist), name_next, pt_next[0], pt_next[1], dt_exp, dt_real, abs(dt_exp-dt_real)))

    scheduler.plot()



