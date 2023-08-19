#!/usr/bin/python3
"""
MeerKAT Extension (MKE)
(r)emote (i)nterface (m)anagement (lib)rary
interface library for accessing remote experiment and analysis data in a dbserver
"""

import copy
import requests
import inspect

import datetime
import time

import os
import json

import logging
import sys
import gzip
import pickle
import io

_log = logging.getLogger()
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
_log.addHandler(streamHandler)

from mke_client.helpers import get_utcnow, make_zulustr, parse_zulutime, join, mkdir


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    
def print_red(msg):
    print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")

def print_color(msg, color=bcolors.ENDC):
    print(f"{color}{msg}{bcolors.ENDC}")



allowed_status_codes = {

    'INITIALIZING': 0,
    'AWAITING_CHECK': 1,
    'WAITING_TO_RUN': 2,
    'HOLD': 3,
    
    'STARTING': 10,
    'RUNNING': 11,
    'CANCELLING': 12,
    'FINISHING': 13,

    'AWAITING_POST_PROC': 100,

    'FINISHED': 100,
    'ABORTED': 101,

    'CANCELLED': 1001,
    'FAILED': 1000,
    'FAULTY': 1002,
}

dc_antennas = {
    'localhost': 'localhost',
    'test_antenna': '<no-ip-needed>',
    'test-antenna': '<no-ip-needed>',
    'skampi': '10.96.64.10',
    'sim-bonn': '134.104.22.44',
    'sim_bonn': '134.104.22.44'
    }

dc_antennas = {
    'sim_bonn': {
            'address': dc_antennas['sim-bonn'],
            'altitude': 1086,
            'comments': 'ACU/SCU simulator running on seperate PC in Bonn',
            'configuration': 'sim-bonn',
            'id': 's999',
            'lat': -30.7249,
            'lon': 21.45714,
            'params_json': '',
            'params_json_hist': '',
            'software_version': '001'
            },
    'test_antenna': {
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
}

dc_antennas['test-antenna'] = dc_antennas['test_antenna']
dc_antennas['sim-bonn'] = dc_antennas['sim_bonn']



def print_sys_info():
    try:
        import platform
        from psutil import virtual_memory
        import getpass
        import datetime
        import time

        username = getpass.getuser()
        now = datetime.datetime.now()
        mem = virtual_memory()
        uname = platform.uname()

        print("="*40, "System Information", "="*40)
        print("")
        print(f"User:      {username}")
        print(f"System:    {uname.system}")
        print(f"Node Name: {uname.node}")
        print(f"Release:   {uname.release}")
        print(f"Version:   {uname.version}")
        print(f"Machine:   {uname.machine}")
        print(f"Processor: {uname.processor}")
        print("RAM:       {:.1f} GB".format(mem.total / (1024 * 1024 * 1024)))
        print ("\n")
        print("Current date and time : " + now.strftime("%Y-%m-%d %H:%M:%S"))
        print("                  ISO : " + datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())
        print('')
        print("="*40, "System Information", "="*40)
    except Exception:
        print_red('Error while trying to print system info')


def __run_fun___(fun, dc, *args, **kwargs):
    if not fun is None and hasattr(fun, '__call__'):
        dc = fun(dc, *args, **kwargs)
        assert isinstance(dc, dict), 'return type dict was expeted from function, but atual return type was: ' + str(type(dc))
    return dc

def wait_for_start_condition(start_condition, wait_increment_max=10, verb=True):
    dt_start = parse_zulutime(start_condition)
    

    t_rem = (dt_start - get_utcnow() ).total_seconds()
    if t_rem <= 0:
        return

    t_rem = max(1, t_rem + 1)
    
    if verb:
        print('Waiting for start condition: "{}" (~{}s)'.format(start_condition, int(t_rem)))

    while t_rem > 0:
        t_wait = min(wait_increment_max, t_rem) 
        time.sleep(t_wait)
        t_rem -= t_wait



class BaseRimObj():
    """base object to have the Analysis and Experiment 
    classes inherit from
    """
    def __init__(self, uri, tablename, id):
        self.uri = uri
        self.__tablename = tablename
        self.id = id

    @property
    def tablename(self):
        """this objects associated table name"""
        return self.__tablename

    def get(self, tablename=None, id=None, **kwargs):
        id = self.id if id is None else id
        tablename = self.tablename if not tablename else tablename

        r = requests.get(f'{self.uri}/{tablename}/{id}', **kwargs)
        assert r.status_code  == 200, r.text
        return r.json()

    def patch_me(self, **kwargs):
        r = requests.patch(f'{self.uri}/{self.tablename}/{self.id}', **kwargs)
        assert r.status_code < 300, r.text
        return r.json()

    def post(self, route, **kwargs):
        r = requests.post(f'{self.uri}/{route}', **kwargs)
        assert r.status_code < 300, r.text
        return r.json()

    def get_me(self) -> dict:
        """returns the database entry row associated with this objects id as dictionary"""
        return self.get()

    def get_my_antenna(self) -> dict:
        """returns the antenna entry row associated with this objects antenna_id as dictionary"""
        me = self.get() 
        return self.get('antennas', me['antenna_id'])

    def get_my_antenna_url(self) -> dict:
        """returns the antenna entry row associated with this objects antenna_id as dictionary"""
        antenna = self.get_my_antenna()
        antenna_url = str(antenna['address'])

        if not ':' in antenna_url:
            antenna_url = antenna_url + ':8080'
        if not antenna_url.startswith('http'):
            antenna_url = 'http://' + antenna_url
        return antenna_url

    def get_my_antenna_ip(self) -> str:
        """returns the antenna entry row associated with this objects antenna_id as dictionary"""
        antenna = self.get_my_antenna()
        antenna_ip = str(antenna['address'])
        return antenna_ip


    def set_status(self, new_status:str, ignore_enum=False) -> dict:
        """set a new status to my object in the DB and return the updated 
        remote object as dictionary.

        Example::
            The status must be one of::

                INITIALIZING, AWAITING_CHECK, WAITING_TO_RUN, HOLD, STARTING, 
                RUNNING, CANCELLING, FINISHING, FINISHED, ABORTED, CANCELLED, 
                FAILED, FAULTY

            but ideally you should only set RUNNING, or FINISHING. See::
            
                .set_status_finishing()
                .set_status_running()

        Args:
            new_status (str): the new status to set. See above
            ignore_enum (bool, optional): set True to not check if the new status is allowed. Defaults to False.

        Returns:
            dict: the database entry row associated with this objects id as dictionary
        """
        assert new_status in allowed_status_codes or ignore_enum, "the given status was not within the allowed status strings: allowed are: " + ', '.join(allowed_status_codes.keys())
        return self.patch_me(json=dict(status=new_status))


    def set_status_cancelling(self) -> dict:
        """set CANCELLING as new status to my object in the DB and return the updated 
        remote object as dictionary.

        Returns:
            dict: the database entry row associated with this objects id as dictionary
        """
        return self.set_status('CANCELLING')


    def set_status_finishing(self) -> dict:
        """set FINISHING as new status to my object in the DB and return the updated 
        remote object as dictionary.

        Returns:
            dict: the database entry row associated with this objects id as dictionary
        """
        return self.set_status('FINISHING')

    def set_status_running(self) -> dict:
        """set RUNNING as new status to my object in the DB and return the updated 
        remote object as dictionary.

        Returns:
            dict: the database entry row associated with this objects id as dictionary
        """
        return self.set_status('RUNNING')

    def check_for_cancel(self) -> bool:
        """gets the remote table row associated with me and returns whether or not a cancel was requested
        
        Returns:
            bool: true if cancel was requested, false if not
        """
        me = self.get()
        assert me['status'] in allowed_status_codes, 'ERROR! The remote status ' + me['status'] + ' is unrecognized'
        return allowed_status_codes[me['status']] >= 100 or me['status'] == 'CANCELLING'

    
    def get_remaining_time(self, t_is: datetime.datetime = None) -> float:
        """gets my remote object and checks how much time it 
        is allowed to be running by returning
            (start_condition + duration_expected) < utcnow

        Returns:
            float: the remaining time in hours for this script to run
        """
        me = self.get()
        if 'end_condition' in me and me['end_condition']:
            t_end_req = parse_zulutime(me['end_condition'])
        else:
            return 1024
        
        assert t_end_req is not None, '"end_condition" could not be parsed. Got: {} {}'.format(type(me['end_condition']), me['end_condition'])

        if t_is is None:
            t_is = get_utcnow()
        if not isinstance(t_is, datetime.datetime):
            # must be astropy time try casting to datetime.datetime
            t_is = t_is.datetime

        t_rem = (t_end_req - t_is).total_seconds() / 60.0 / 60.0
        return max(0, t_rem)


    def wait_for_start_condition(self, wait_increment_max=10, verb=True):
        dc = self.get()
        wait_for_start_condition(dc['start_condition'], wait_increment_max,  verb)


#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################


    def run_experiment(self, f_init=None, f_get_time = None, f_tick=None, f_finish=None, is_dryrun=True, n_ticks_max=float("inf"), verbose=True, skip_faulty_ticks=True, **kwargs):
        """run an experiment either with, or without being connected to a remote measurement database.

        for all function handles passed to this function as arguments, the signature is:
            variable_which_is_dict = fun(variable_which_is_dict)
        all data which need to be transferred or saved can be stored in the dict which is passed and returned

    Args:
        exp:Experiment=None
        f_init (function handle, optional): The function to call for initialization. Defaults to None.
        f_get_time (function handle, optional): The function which to call to return the ACU/SCU timestamp now (as astropy time). Defaults to None.
        f_tick (function handle, optional): The function to call for each tick of the measurement (THIS IS THE MAIN FUNCTION TO HANDLE MEASURING). Defaults to None.
        f_finish (function handle, optional): The function to call after finishing the measurement process (usualy for antenna stowing/shutdown). Defaults to None.
        is_dryrun (bool, optional): True to not save data and indicate that this is a testrun. Defaults to True.
        n_ticks_max (_type_, optional): number of calls to function f_tick max. Defaults to float("inf").
        ignore_time (bool, optional): True in order to ignore any stopping time and just run until the script has finished. Defaults to True.
        verbose (bool, optional): Set True to increase the amount of output text. Defaults to True.
        skip_faulty_ticks (bool, optional): _description_. Defaults to True.
    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
        
        # if not verbose:
        #     def print_dummy(*args, **kwargs):
        #         pass        
        #     print = print_dummy
        dc = {}

        if not f_init is None and hasattr(f_init, '__call__'):
            print(make_zulustr(get_utcnow()) + ' | Initializing...')
            dc = __run_fun___(f_init, dc)

        t_start = get_utcnow()
        print(make_zulustr(get_utcnow()) + ' | Starting...')

        if inspect.isgeneratorfunction(f_tick):
            ticker = f_tick(dc)   
        else:
            ticker = None

        tickcount = 0
        try:
            self.set_status_running()
            
            
            while tickcount < n_ticks_max: 
                try:
                    tickcount += 1
                    
                    # ---------------------------------------
                    # wait for my start condition
                    # ---------------------------------------
                    if hasattr(self, 'wait_for_start_condition'):
                        self.wait_for_start_condition()
                    
                    # ---------------------------------------
                    # check if I should stop
                    # ---------------------------------------

                    if not is_dryrun and self.get_remaining_time(f_get_time()) <= 0:
                        print(make_zulustr(get_utcnow()) + ' | Time is up... finshing')
                        my_row_as_dict = self.set_status_finishing()
                        break

                    if not is_dryrun and self.check_for_cancel():
                        print(make_zulustr(get_utcnow()) + ' | Cancle initiated from externally... cancelling')
                        my_row_as_dict = self.set_status_cancelling()
                        break

                    # ---------------------------------------
                    # perform the test
                    # ---------------------------------------

                    if f_tick is None:
                        pass
                    elif ticker is not None:
                        try:
                            print(make_zulustr(get_utcnow()) + ' | Calling next(tick)...')
                            dci = next(ticker)
                            assert isinstance(dci, dict), 'expected dict return type for tick iterator'
                            if dci != dc:
                                dc = {**dc, **dci}
                        except StopIteration:
                            print(make_zulustr(get_utcnow()) + ' | Last Iteration Reached... stopping loop')
                            break
                    elif hasattr(f_tick, '__call__'):
                        print(make_zulustr(get_utcnow()) + ' | Calling tick()...')
                        dc = __run_fun___(f_tick, dc)
                    else:
                        raise Exception('f_tick is neither None, nor an iterator, nor a function handle. But one of the three was expected')


                    print(make_zulustr(get_utcnow()) + f' | completed tick {tickcount} ...')
                except Exception as err:
                    if skip_faulty_ticks:
                        print_red('ERROR: ' + str(err))
                    else:
                        raise


            t_end = get_utcnow()
            t_elapsed = t_end - t_start
            my_row_as_dict = self.set_status('AWAITING_POST_PROC')

            print(make_zulustr(get_utcnow()) + f' | Finished main loop (t_elapsed={t_elapsed})') 
            
            
        except Exception as err:
            print_red('ERROR: ' + str(err))
            raise
        finally:
            # ---------------------------------------+
            # shutdown the antenna
            # ---------------------------------------
            dc = __run_fun___(f_finish, dc)
            

        return my_row_as_dict, t_elapsed, dc

        
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################





class Experiment(BaseRimObj):
    """An interface object to get access to experiments in the 
    database.

    Args:
        RimObj: _description_
    """
    __tablename = 'experiments'


    def __init__(self, id, uri = None, allow_fallback_local=True, dc=None, is_dryrun=False):
        """create a new Experiment object with an id to get access 
        to this expiriment objects row in the database

        Args:
            id (int): the id of the analyses in the DB
            uri (string, optional): the URI to connect to. 
                If not given will be tried to be resolved 
                from environmental valiables.
                    Defaults to None.
        """
        if uri is None:
            uri = os.environ.get('DBSERVER_URI')
        assert uri or id < 0, 'need to give a valid URI for a DB connection!'
        
        self.allow_fallback_local = allow_fallback_local
        self.savedir = ''
        self.is_dryrun = is_dryrun
        self.__dc = {}
        self.__data_df = {}
        self.__meas_data = []

        super().__init__(uri, self.__tablename, id)


        if self.is_dryrun or self.test_local():
            if 'script_out_path' in dc:
                self.savedir = os.path.dirname(dc['script_out_path']) 
                
            dc['time_started_iso'] = make_zulustr(get_utcnow())
            if self.is_dryrun:
                self.__dc = {**self.__dc, **dc}
            else:
                self.__commit(dc)


    
    def __commit(self, dc):
        
        dbpath = join(self.savedir, self.tablename + '.json')
        if os.path.exists(dbpath):
            with open(dbpath, 'r') as fp:
                db = json.load(fp)
        else:
            db = {}
        
        db = {**db, **dc}
        
        with open(dbpath, 'w+') as fp:
            json.dump(db, fp, indent=3)

        return db
            

    def test_local(self, id=None):
        if (id is None or id < 0) and (self.id is None or self.id < 0):
            return True
        return False

    def get(self, tablename=None, id=None, **kwargs):
        if self.is_dryrun:
            return {k:v for k, v in self.items()}
        elif self.test_local(id):
            tablename = self.tablename if not tablename else tablename
            id = self.id if id is None else id
            with open(join(self.savedir, tablename + '.json'), 'r') as fp:
                return json.load(fp)
        else:
            return super().get(tablename, id, **kwargs)

    def patch_me(self, **kwargs):
        if self.is_dryrun:
            self.__dc = {**self.__dc, **kwargs['json']}
            return {**self.__dc, **kwargs['json']}
        elif self.test_local():
            return self.__commit(kwargs['json'])
        else:
            return super().patch_me(**kwargs)
    
    def get_my_antenna(self) -> dict:
        if self.is_dryrun or self.test_local():
            me = self.get_me()
            assert me['antenna_id'] in dc_antennas, me['antenna_id'] + ' is not contained within the offline available antenna info'
            return dc_antennas[me['antenna_id']]
        else:
            return super().get_my_antenna()
    
    def get_my_antenna_url(self) -> dict:
        if self.test_local() or self.is_dryrun:
            return f'http://{self.get_my_antenna_ip()}:{8080}'
        else:
            return super().get_my_antenna_url()


    def get_my_antenna_ip(self) -> str:
        if self.is_dryrun or self.test_local():
            self.get_my_antenna()['address']
        else:
            return super().get_my_antenna_ip()
        
    def ping_test(self):
        """will ping the DB server and return if successful
        """
        if self.is_dryrun:
            return False
        try:
            r = requests.get(f'{self.uri}/ping', timeout=2)
            return r.status_code <= 200
        except Exception as err:
            _log.error('Error while pinging: ' + str(err))
            return False



    def upload_new_dfs(self, df_dict):
        """upload a new set of dataframes to the time series database 
        for later usage in post processing. 

        Args:
            df_dict (dict str:pd.DataFrame): a dict with the dataframes to upload and meas_name as keys

        Returns:
            dict str:int -> meas_name as keys, counts of rows written as values
        """

        for df in df_dict.values():
            assert hasattr(df, 'index') and hasattr(df, 'values') and hasattr(df, 'columns'), 'expected dataframe type, but got: ' + str(type(df))
            assert hasattr(df.index, 'to_pydatetime'), 'expected datetime index for dataframe, but got: ' + str(type(df.index)) # isinstance pd.DatetimeIndex
        
        if self.is_dryrun or self.test_local():
            return self.save_dfs_local(df_dict)

        try:
            files = {}
            for k, df in df_dict.items():
                bts = gzip.compress(gzip.compress(pickle.dump(df)))
                iobuff = io.BytesIO(bts)
                files[k] = iobuff
            me = self.get_me()
            dc = self.post('upload_df', files=files, json=dict(antenna_id=me['antenna_id']))
        except Exception as err:
            if self.allow_fallback_local:
                _log.error('ERROR while uploading!')
                _log.error(err)
                _log.error('Falling back to local!')
                self.save_dfs_local(df_dict)
                
            else:
                raise    
            
        return dc
    
    def save_dfs_local(self, df_dict, timeformat_str = '%Y%m%d_%H%M%S'):
        """save a new set of dataframes to the local filesys as csvs (usually as fallback
        in case there is no server connection.)
        

        Args:
            df_dict (dict str:pd.DataFrame): a dict with the dataframes to upload and meas_name as keys
            timeformat_str (str, optional): strftime format for the leading timestamp when creating a file name. Defaults to '%Y%m%d_%H%M'.
        """          
        ret = {}  
        for meas_key, df in df_dict.items():
            t0 = df.index.min()
            
            fname = t0.strftime(timeformat_str) + '_' + meas_key + '.csv'
            folderpath = join(self.savedir, 'data_raw')
            f = join(folderpath, fname)
            ret[meas_key] = len(df)
            if self.is_dryrun:
                self.__data_df[f] = df
            else:
                mkdir(folderpath)
                _log.info('saving --> ' + f)
                df.to_csv(f)
        return ret

    
    def upload_new_df(self, df, meas_name):
        """upload a new dataframe to the time series database for later usage in post processing.

        Args:
            df (pandas.DataFrame): the pandas dataframe to upload, which must have a DateTime index
            meas_name (str): measurement series name, such as 'ACU', 'STR' etc.

        Returns:
            int -> count of rows written
        """

        assert hasattr(df, 'index') and hasattr(df, 'values') and hasattr(df, 'columns'), 'expected dataframe type, but got: ' + str(type(df))
        assert hasattr(df.index, 'to_pydatetime'), 'expected datetime index for dataframe, but got: ' + str(type(df.index)) # isinstance pd.DatetimeIndex
        
        return self.upload_new_dfs(self, dict((meas_name, df)))
        
    def register_measurement(self, t0:datetime.datetime, t1:datetime.datetime, devices:list=None, tags:list=None):
        """register a given period of time as measurement data (the actual data will be retrieved from the 
        timeseries database. Use upload_new_df() to add the data to the time series db)

        Args:
            t0 (datetime.datetime): start time
            t1 (datetime.datetime): end time
            devices (list, optional): list of strings holding the meas_names associated devices to add. Defaults to None.
            tags (list, optional): list of strings with any arbitrary tags you want to add to this measurement. Defaults to None.
        
        Returns:
            int -> the id of the new measurement_data object created. Can be accessed by url+ + '/measurement_data/id'
        """
        def parse(t):
            if not isinstance(t, datetime.datetime) and hasattr(t, 'datetime'):
                t = t.datetime  # must be astropy. try parse
            elif not isinstance(t, datetime.datetime) and hasattr(t, 'to_pydatetime'):
                t = t.to_pydatetime() # must be pandas. try parse
            elif isinstance(t, datetime.datetime):
                pass
            elif isinstance(t, str):
                t = parse_zulutime(t)
            else:
                raise ValueError(f'could not parse dataobject of type {type(t)} to datetime!')
            return t
        
        t0, t1 = make_zulustr(parse(t0)), make_zulustr(parse(t1))
        t0, t1 = min(t0, t1), max(t0, t1)

        row = {
            'time_start': t0,
            'time_end': t1,
        }
        
        
        if devices:
            assert isinstance(devices, list), 'devices is not a list of strings! got: ' + str(devices)
            assert all([isinstance(v, str) for v in devices]), 'devices is not a list of strings! got: ' + str(devices)
            row['devices'] = devices

        if tags:
            assert isinstance(tags, list), 'tags is not a list of strings! got: ' + str(tags)
            assert all([isinstance(v, str) for v in tags]), 'tags is not a list of strings! got: ' + str(tags)
            row['tags'] = tags
        
        if self.is_dryrun:
            self.__meas_data.append(row)
        elif self.test_local():
            s = json.dumps(row)
            _log.info('REGISTERING measurement_data:')
            _log.info(s)
            dbpath = dbpath = join(self.savedir, 'measurement_data.jsonlines')
            with open(dbpath, 'a+') as fp:
                fp.write(s + '\n')
        else:
            return self.post('register_result', json=row)
    
    def get_dryrun_data(self):
        return self.__meas_data, self.__data_df