
import datetime
import dateutil
import pytz

import re

# import datetime
import os

import re
import dateutil.parser, datetime, time, pytz

import logging
import sys

_log = logging.getLogger()
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
_log.addHandler(streamHandler)


from pathlib import Path
home = str(Path.home())

# if __name__ == '___main__':
#     import sys, inspect, os
#     # path was needed for local testing
#     current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#     parent_dir = os.path.dirname(current_dir)
#     sys.path.insert(0, parent_dir)




def get_utcnow():
    """get current UTC date and time as datetime.datetime object timezone aware"""
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

def make_zulustr(dtobj:datetime.datetime, remove_ms = True) -> str:
    '''datetime.datetime object to ISO zulu style string
    will set tzinfo to utc
    will replace microseconds with 0 if remove_ms is given

    Args:
        dtobj (datetime.datetime): the datetime object to parse
        remove_ms (bool, optional): will replace microseconds with 0 if True . Defaults to True.

    Returns:
        str: zulu style string e.G. 
            if remove_ms: 
                "2022-06-09T10:05:21Z"
            else:
                "2022-06-09T10:05:21.123456Z"
    '''
    utc = dtobj.replace(tzinfo=pytz.utc)
    if remove_ms:
        utc = utc.replace(microsecond=0)
    return utc.isoformat().replace('+00:00','') + 'Z'

def parse_zulutime(s:str)->datetime.datetime:
    '''will parse a zulu style string to a datetime.datetime object. Allowed are
        "2022-06-09T10:05:21.123456Z"
        "2022-06-09T10:05:21Z" --> Microseconds set to zero
        "2022-06-09Z" --> Time set to "00:00:00.000000"
    '''
    try:
        if re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}Z', s) is not None:
            s = s[:-1] + 'T00:00:00Z'
        return dateutil.parser.isoparse(s).replace(tzinfo=pytz.utc)
    except Exception:
        return None


def mkdir(pth, raise_ex=False, verbose=False):
    try:
        if not os.path.exists(pth):
            if verbose:
                _log.info('Creating dir because it does not exist: ' + pth)
            os.makedirs(pth, exist_ok=True)
            path = Path(pth)
            path.mkdir(parents=True, exist_ok=True)
            return str(path).replace('\\', '/').replace('//', '/')

    except Exception as err:
        _log.error(err)
        if raise_ex:
            raise
    return None

def join(*parts):
    return os.path.join(*parts).replace('\\', '/').replace('//', '/')