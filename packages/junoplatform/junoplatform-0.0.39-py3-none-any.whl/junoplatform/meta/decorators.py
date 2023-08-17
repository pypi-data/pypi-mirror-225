"""decorators.py: decorator class and functions for junoplatform"""

__author__      = "Bruce.Lu"
__email__       = "lzbgt@icloud.com"
__time__ = "2023/07/20"

import numpy as np
from threading import Thread
from junoplatform.io import InputConfig, Storage, DataSet
from junoplatform.io.utils import junoconfig
from junoplatform.log import logger
from functools import wraps
import datetime
import time
import os
import json
import traceback

class EntryPoint:
    def __init__(self, cfg_in: str|InputConfig, detached: bool = False):
        super(EntryPoint, self).__init__()
        self.cfg_in: InputConfig
        self.detached = detached
        self.storage = Storage()
        self.dataset = DataSet()
        self.algo_cfg = junoconfig["algo_cfg"]
        if isinstance(cfg_in, str):
            logger.debug(f"loading input spec from file: {cfg_in}")
            try:
                self.cfg_in = InputConfig(**json.load(open(cfg_in)))
            except Exception as e:
                msg = f"error in input.json: {e}"
                logger.error(msg)
                exit(1)
        elif isinstance(self.cfg_in, InputConfig):
            logger.info(f"loading input spec from class: {cfg_in}")
            self.cfg_in = cfg_in
        else:
            raise Exception(f"cfg_in must be type of InputConfig or string, but provides: {type(self.cfg_in)}")

    def __call__(self, func):
        def thread():
           while True:
              logger.info(f"running algo with junoconfig {junoconfig}")
              ts = datetime.datetime.now().timestamp()
              if self.cfg_in.items:
                data, timestamps, names = self.dataset.fetch(tags=self.cfg_in.tags, num=self.cfg_in.items)
              elif self.cfg_in.minutes:
                    time_from = datetime.datetime.now() - datetime.timedelta(minutes=self.cfg_in.minutes)
                    data, timestamps, names = self.dataset.fetch(tags=self.cfg_in.tags, time_from=time_from)
              else:
                  raise Exception("invalid InputConfig")
              
              td = datetime.datetime.now().timestamp()
              logger.info(f"time used fetching dataset: {td-ts}s")
              
              try:
                func(self.storage, self.algo_cfg, data, timestamps, names)
              except Exception as e:
                msg = traceback.format_exc()
                logger.error(f"{e}: {msg}")
                
              # TODO: output
              te = datetime.datetime.now().timestamp()
              logger.info(f"time used running algo: {te-td}s")

              delay = self.cfg_in.sched_interval - (te -ts) - 0.003
              logger.debug(f"delay in seconds to make up a full sched_interval: {delay}")
              if delay < 0: 
                 delay = 0
              time.sleep(delay)
              
        th = Thread(target=thread)
        if self.detached:
            th.daemon = True
        th.start()
        if not self.detached:
            th.join()

def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(args[0].juno_dir) or not os.path.exists(args[0].juno_file):
            logger.error(f"user not authenticationd.\n\
                          please run `junocli login [api_url]` to use your shuhan account")
            os.makedirs(args[0].juno_dir, exist_ok=True)
            return -1
        return func(*args, **kwargs)
        
    return wrapper