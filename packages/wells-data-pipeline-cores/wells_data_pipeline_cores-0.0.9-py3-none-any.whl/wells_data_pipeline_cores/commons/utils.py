from datetime import datetime, timedelta
from dateutil import parser
import time
import pytz

import pytz

from typing import (
    Text,
    Any,
    Union
)

import warnings
import contextlib

import requests
from urllib3.exceptions import InsecureRequestWarning

old_merge_environment_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass
            
class Utils():
    
    @staticmethod
    def get_dict_val(data:dict, key:str=None, key_path:str=None, default=None):
        """
        Params:
            - data: is dict object
            - key (optional): get dict value by key
            - key_path (optional): get value of nested dict object. e.g.: key1.key2.key3
        Returns:
            - Value if found, None othewise
        """
        if data is not None and key is not None:
            try:
                return data.get(key, default)
            except:
                pass

        if data is not None and key_path is not None:
            try:
                keys = key_path.split(".")
                value = default
                obj_value = data
                for key in keys:
                    if isinstance(obj_value, dict):
                        value = obj_value.get(key)
                        obj_value = value
                    else:
                        return default
                return value
            except Exception as ex:
                pass

        return default
    
    @staticmethod
    def to_datetime(dtime:Union[str, datetime]) -> datetime:
        """
        Params:
            - dtime: string date time
        Return:
            - datetime object. It will convert to UTC if there is no timezone in dtime text
        """
        if dtime is None or len(dtime) == 0:
            return None

        try:           
            if isinstance(dtime, datetime):
                obj_dtime = dtime
            else:
                obj_dtime = parser.parse(dtime)

            if obj_dtime.tzinfo is None:
                utc = pytz.UTC
                obj_dtime = utc.localize(obj_dtime)

            return obj_dtime
        except:
            pass

        return None

    @staticmethod
    def to_datetime_from_timestamp(timestamp:Union[str, int, float]) -> datetime:
        """
        Params:
            - timestamp: is in the seconds or millis-seconds
        Return:
            - datetime object with timezone utc
        """
        try:
            if timestamp is not None:
                if isinstance(timestamp, str):
                    ts_date = float(timestamp)
                elif isinstance(timestamp, int) or isinstance(timestamp, float):
                    ts_date = timestamp

                HUNDRED_YEARS = 100 * 365 * 24 * 3600
                if ts_date > time.time() + HUNDRED_YEARS:
                    # process miliseconds
                    _millis = ts_date % 1000
                    _ts_sec = ts_date / 1000

                    utc_dtime = (datetime.utcfromtimestamp(_ts_sec) + timedelta(milliseconds=_millis))
                else:
                    # process seconds
                    utc_dtime = datetime.utcfromtimestamp(ts_date)  
                
                # add aware timezone utc
                utc = pytz.UTC
                return utc.localize(utc_dtime)
        except Exception as ex:
            # print(f"to_datetime_from_timestamp - {ex}")
            pass
        return None

    @staticmethod
    def to_timestamp(dtime:datetime):
        """
        Params:
            - dtime: datetime object
        Return:
            - unix timestamp in millis seconds
        """
        try:
            if dtime is not None:
                unix_timestamp = datetime.timestamp(dtime)*1000
                return unix_timestamp

        except Exception as ex:
            pass
        return None