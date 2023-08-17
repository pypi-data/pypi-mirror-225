from junoplatform.meta.decorators import EntryPoint
from junoplatform.io import *
from junoplatform.log import logger
import random
import json

#@EntryPoint(InputConfig(tags=["AI-T20502_DIS", "AI-T20501_DIS"], items=1440, interval=5), detached=False)
@EntryPoint("input.json", detached=False)
def any_algo_entry_func(storage:Storage, algo_cfg, data, timestamps, names):
    ''' params signature of algo func:
    storage: Storage
      framework provided storage object
    algo_cfg: dict
      algo configration from config.json
    data: numpy.ndarray
      framework provided input dataset which specified by `InputConfig` or input.json
    timestamps: List[datetime.datetime]
      timestamps for data
    names: List[str]
      col names for data
    '''

    # demo: algo processing with input data here
    logger.info(f"processing data: {data.shape}, tags: {names}, time: {timestamps[0]} ~ {timestamps[-1]}")
    
    # demo: construct results as list of dict: [{"key": key, "value": value}]
    opc_data = [{"key": f"{names[0]}", "value": random.randint(1,10)}, {"key": f"{names[1]}", "value": random.randint(1,10)}]
    probe1 = {"pX":random.randint(1,10)}
    state1 = {'pY': 1}

    # demo: algo oputput results
    logger.info("data processed, writing outputs:")
    # write data to cloud
    storage.cloud.write("probe1", probe1)

    # write data to opc
    storage.opc.write(opc_data)

    # read/write data to local
    storage.local.write('state1_bytes', json.dumps(state1).encode(), isBytes=True)
    data = storage.local.read('state1_bytes', isBytes=True)
    logger.info(f"read write bytes: {data}")

    storage.local.write('state1_dict', state1)
    data = storage.local.read('state1_dcit')
    logger.info(f"read write dict: {data}")