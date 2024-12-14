import logging
import logging.config
from typing import Union
from gdx import gdx
from multiprocessing import Pool, Value
from time import sleep

# setup loggers
logging.config.fileConfig('log.ini', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.

gdx = gdx.gdx() 
gdx.open(connection='ble',device_to_open='GDX-FP 1J1000T6')
# sensor type: Force
gdx.select_sensors([1])
# sample rate: 1ms 
gdx.start(1)
column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
logger.info('\n')
logger.info(column_headers)

for i in range(0,1000):
    measurements = gdx.read()
    if measurements == None:
        break 
    logger.info(measurements)

gdx.stop()
gdx.close()