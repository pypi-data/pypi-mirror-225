"""junoplatform.io: implements io spec and common tools for algo"""
__author__      = "Bruce.Lu"
__email__       = "lzbgt@icloud.com"
__time__ = "2023/07/20"

__all__ = [
    'Storage',
    'InputConfig',
]

from pydantic import BaseModel, Field, model_validator, NonNegativeInt
import datetime as datetime
from typing import Optional, Any, List
import numpy as np

from junoplatform.io._driver import Pulsar as Pulsar, Opc as Opc, junoconfig, Redis, Clickhouse, RDLock
from junoplatform.io.utils import junoconfig
import logging


class InputConfig(BaseModel):
    ''' InputConfig spec for JunoPlatform Runtime
    tags: OPC tags
    minutes: last n minutes of data
    items: last n records of data
    sched_interval: algo schedule interval in seconds
    '''
    tags: List[str]
    minutes: Optional[NonNegativeInt] = Field(default=None, description='input data of last n minutes')
    items: Optional[NonNegativeInt] = Field(default= None, description='input data of last n items')
    sched_interval: NonNegativeInt = Field(description='schedule interval in seconds')

    @model_validator(mode="before")
    def atleast_one(cls, values: 'dict[str, Any]') -> 'dict[str, Any]':
        if not values.get('minutes') and not values.get('items'):
            raise ValueError("field 'minutes' or 'items' must be given")
        return values

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class DataSet():
    def __init__(self) -> None:

        if 'clickhouse' in junoconfig:
            self.url = junoconfig['clickhouse']['url']
        else:
            devcfg = {'gangqu': 'ch://sf_read1:reader@123.@192.168.101.101:7000', 
                      'yudai': 'ch://default:L0veclickhouse@192.168.101.101:8123',
                      'yulin':'ch://sf_read1:reader@123.@192.168.101.101:7010'}
            self.url = devcfg[junoconfig["plant"]]
        self.io:Clickhouse = Clickhouse(url=self.url)
        self.tbl_c = f'{junoconfig["plant"]}_data.running'
        self.tbl_w = f'{junoconfig["plant"]}_data.running_today'

    def fetch(self, num:int = 0, tags:List[str] = "", time_from = None):
        if num >0:
            data, timestamps, names = self.io.read(self.tbl_w, tskey='time', tags=tags, num = num, time_from=None)
            num = num - len(timestamps)
            if num > 0:
                nd, nt, _ = self.io.read(self.tbl_c, tskey='time', tags=tags, num = num, time_from=None)
                return np.concatenate((nd, data), axis=0), nt + timestamps, names
            return data, timestamps, names
        if time_from:
            data, timestamps, names = self.io.read(self.tbl_w, tskey='time', tags=tags, num = 0, time_from=time_from)
            if timestamps[0] > time_from:
                nd, nt, _ = self.io.read(self.tbl_c, tskey='time', tags=tags, num = 0, time_from=time_from)
                return np.concatenate((nd, data), axis=0), nt + timestamps, names
            return data, timestamps, names


class Storage(metaclass=Singleton):
    _cloud = None
    _opc = None
    _local = None

    def __init__(self):
        super(Storage, self).__init__()
        _redis_cfg = junoconfig['redis']
        self._local = Redis(**_redis_cfg)
        self.lock = RDLock(self._local.io)

    @property
    def cloud(self):
        if not self._cloud:
            CloudStorage:Pulsar = Pulsar(**junoconfig['pulsar'], lock=self.lock)
            self._cloud = CloudStorage
        return self._cloud
    
    @property
    def opc(self):
        if not self._opc:     
            OpcWriter = Opc(lock=self.lock)
            self._opc = OpcWriter  
        
        return self._opc
    
    @property
    def local(self):
        return self._local
