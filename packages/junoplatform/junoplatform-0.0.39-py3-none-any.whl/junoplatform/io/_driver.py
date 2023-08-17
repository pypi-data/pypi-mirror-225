"""junoplatform.io._driver.py: implements DB adaptor classes"""
__author__      = "Bruce.Lu"
__email__       = "lzbgt@icloud.com"
__time__ = "2023/07/20"

from abc import ABC, abstractmethod
import itertools
from junoplatform.io.utils import *
import logging
from typing import Dict
from pulsar import Client, AuthenticationTLS, ConsumerType, InitialPosition, schema, Producer, Consumer
import json
from datetime import datetime
from typing import List
import dateparser
import numpy as np
from junoplatform.api.local import write as connector_write
import redis

class IWriter(ABC):
    @abstractmethod
    def write(self, **kwargs):
        pass

class IReader(ABC):
    @abstractmethod
    def read(self, **kwargs):
        pass

class ALock(ABC):
    @abstractmethod
    def aquire(self, key:str, ex:int):
        pass


class RDLock(ALock):
    def __init__(self, redis:redis.Redis):
        super(RDLock, self).__init__
        self.redis = redis
        self.key = f"{junoconfig['plant']}.{junoconfig['module']}.rdlock"
        marg = junoconfig['input_cfg']["sched_interval"]/3
        if marg < 13:
            marg = 13
        self.ex = junoconfig['input_cfg']["sched_interval"] + marg
        
        self.uid:str = junoconfig['instance_id']

    def aquire(self):
        try:
            if "." not in self.uid:
                return True
            
            r = self.redis.setnx(self.key, self.uid)
            if not r:
                v = self.redis.get(self.key)
                if v.decode() != self.uid:
                    return False
            self.redis.expire(self.key, self.ex)
            return True
        except Exception as e:
            logging.error({e})
            return False

class Opc(IWriter, IReader):
    def __init__(self, lock:ALock=None ,**kwargs,):
        super(Opc, self).__init__()
        self.io = kwargs
        self.lock = lock
    
    def write(self, data:list[dict], **kwargs):
        if self.lock:
            if not self.lock.aquire():
                logging.warn("holding no lock, skip opc write")
                return
        return connector_write(data)

    def read(self, **kwargs):
        pass

class Pulsar(IWriter, IReader):
    def __init__(self, lock:ALock = None,  **kwargs):
        super(Pulsar, self).__init__()
        self.io = pulsar_cli(**kwargs)
        logging.info(f"pulsar args: {kwargs}")
        self.producers: Dict[str, Producer] = {}
        self.consumers: Dict[str, Consumer] = {}
        self.plant = junoconfig["plant"]
        self.module = junoconfig["module"]
        self.name = f"algo-{self.plant}-{self.module}"
        self.lock=lock

    def write(self, table: str, data:dict, **kwargs):
        if self.lock:
            if not self.lock.aquire():
                logging.warn("holding no lock, skip pulsar write")
                return
            
        topic = f'up-{self.plant}-{self.module}_{table}'
        if not (topic in self.producers):
            self.producers[topic] = self.io.create_producer(topic)

        self.producers[topic].send(json.dumps(data).encode('utf-8'))
        logging.info(f'write cloud: sent {data} to {topic}')
        
    def read(self, topic:str, shared:bool=False):
    #   if self.lock:
    #         if not self.lock.aquire():
    #             logging.warn("holding no lock, skip pulsar read")
    #             return
            
      subtype = ConsumerType.Shared
      if not shared:
          subtype = ConsumerType.Exclusive

      if topic not in self.consumers:
        
        self.consumers[topic] = self.io.subscribe(topic, self.name, 
                              consumer_type=subtype, initial_position=InitialPosition.Latest, 
                              schema=schema.BytesSchema(), pattern_auto_discovery_period=1, broker_consumer_stats_cache_time_ms=1500)
        
      return self.consumers[topic].receive()

class Mongo(IWriter, IReader):
    def __init__(self, **kwargs):
        super(Mongo, self).__init__()
        self.url = kwargs['url']
        self.io = mongo_cli(self.url)
    
    def write(self, table:str, data:dict, **kwargs):
        ''' write to mongodb
            table: str, collection name
            data: dict, document to store
        database is derived from runtime environment
        '''
        logging.info(junoconfig)

        plant = junoconfig['plant']
        module = junoconfig['module']
        self.io[plant][f'{module}_{table}'].insert_one(data)

    def read(self, **kwargs):
        pass

class Redis(IWriter, IReader):
    def __init__(self, **kwargs):
        super(Redis, self).__init__()
        self.io = redis_cli(**kwargs)
        self.lock = RDLock(self.io, )

    def write(self, key: str, value:dict|bytes, isBytes = False, **kwargs):
        if not self.lock.aquire():
            logging.warn("holding no lock, skip redis write")
            return
        
        if isBytes and not isinstance(value, bytes):
            raise Exception("invalid value type")
        if not isBytes:
            logging.info(f"write local:  {key} -> {value}")
            self.io.json().set(key, '$', value)
        else:
            self.io.set(key, value)

    def read(self, key:str, isBytes = False, **kwargs):
        if not isBytes:
            return self.io.json().get(key)
        else:
            return self.io.get(key)

class Elastic(IWriter, IReader):
    def __init__(self, **kwargs):
        super(Elastic, self).__init__()
        self.url = kwargs['url']
        self.ca = kwargs['ca']
        self.user=kwargs['user']
        self.password=kwargs['password']
        self.io:Elasticsearch=es_cli(self.url, ca=self.ca,user=self.user, password=self.password)
    
    def write(self, **kwargs):
        topic=kwargs['topic']
        data=kwargs['data']
        id = ""

        if "et" in data:
            id = str(data["et"])
        
        for x in ["time", "ts", "timestamp"]:
            if id:
                break
            if x in data:
                if isinstance(data[x], str):
                    try:
                        id = str(dateparser.parse(data[x]).timestamp()*1000)
                    except:
                        pass
                elif isinstance(data[x], datetime):
                        id = str(data[x].timestamp()*1000)
            
        if id:
            self.io.index(index=topic, id=id, document=data)
        else:
            self.io.index(index=topic, document=data)
    
    def read(self, **kwargs):
        pass

class Clickhouse(IWriter, IReader):
    def __init__(self, *args, **kwargs):
        super(Clickhouse, self).__init__()
        self.url = kwargs['url']
        self.io: CHClient = clickhouse_cli(self.url)
    
    def write(self, **kwargs):
        pass
    
    def read(self, table:str,  tskey: str, tags:List[str]=[], num=0, time_from = None, time_to = None):
        cols = "*"
        if tags:
            if tskey not in tags:
                tags.append(tskey)
            tags = list(map(lambda x: f"`{x}`", tags))    
            cols = ", ".join(tags)

        sql = f"select {cols} from {table}"
        for x in [time_from, time_to]:
            if isinstance(x, str) or isinstance(x, datetime) or x is None:
                pass
            else:
                raise Exception("invalid time_from or time_to")

        if not time_to and not time_from and not num:
            raise Exception("must provide time_from or time_to or num")
        else:
            s1 = ""
            s2 = ""
            if time_to:
                if isinstance(time_to, datetime):
                    time_to = time_to.strftime("%Y-%m-%d %H:%M:%S")
                s1 = f"{tskey} <= '{time_to}'"
            if time_from:
                if isinstance(time_from, datetime):
                    time_from = time_from.strftime("%Y-%m-%d %H:%M:%S")
                s2 = f"{tskey} > '{time_from}'"
            if s1 and s2:
                sql += f" where {s1} and {s2} "
            else:
                for x in [s1, s2]:
                    if x:
                        sql += f" where {x} "
        order = "asc"
        if num > 0:
            order = "desc"

        sql += f" order by {tskey} {order}"
        if num > 0:
            sql+=f" limit {num}"

        logging.info(sql)
        try:
            r = self.io.query(sql)
            logging.info(f"got {len(r.result_rows)} records from dataset")
            data = list(map(lambda x: x[:-1], r.result_rows))
            timestamps = [x[-1] for x in r.result_rows]
            data = np.array(data,dtype=np.float32)
            column_names = r.column_names[:-1]

            if num > 0:
                timestamps.reverse()
                data = np.flip(data, 0)

            return data, timestamps, column_names
        except Exception as e:
            logging.error(f"exception: {e}")
            return None, None, None

class Qdb(IWriter, IReader):
    def __init__(self, *args, **kwargs):
        super(Qdb, self).__init__()
        self.init_kwargs=kwargs
        self.io = qdb_cli(**self.init_kwargs)
    
    def write(self, **kwargs):
        topic=kwargs['topic']
        data={k.translate(k.maketrans({'-':'_', '.': '_'})):v  for k,v in kwargs['data'].items()}
        buff = self.io.new_buffer()
        buff.row(topic, columns=data)
        self.io.flush(buff)
    
    def read(self, **kwargs):
        pass

def MakeDB(kind: str, **kwargs):
    if kind == 'elastic':
        return Elastic(**kwargs)
    elif kind == 'clickhouse':
        return Clickhouse(**kwargs)
    elif kind == 'qdb':
        return Qdb(**kwargs)
    elif kind == 'mongo':
        return Mongo(**kwargs)
    else:
        raise Exception(f'unkown kind of db: {kind}')