import logging
import logging.config
from gdx import gdx
from time import sleep
import time
import requests
import os
import time
from multiprocessing import Process

# setup loggers
logging.config.fileConfig('plateclient.logconfig', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.
def pass_data_to_server(deviceid, data, cnt, ts):

    # Define the API endpoint
    api_url = f"http://127.0.0.1:8000/add/{deviceid}/data/{data}/cnt/{cnt}/ts/{ts}"
    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code != 200:
        logger.info(f"Error: {response.status_code}")

    return
def pass_buf_to_server(buf):

    newbuf = {'data': buf}
    # Define the API endpoint
    api_url = f"http://127.0.0.1:8000/addbuf/"
    # Make a GET request to the API
    response = requests.post(api_url, json = newbuf)

    # Check if the request was successful
    if response.status_code != 200:
        logger.info(f"Error: {response.status_code}")

    return
def current_milli_time():
    return round(time.time() * 1000)

def func(*buf):
    pass_buf_to_server(buf)

if __name__ == "__main__":
    gdx = gdx.gdx()
    gdx.open(connection='ble',device_to_open='GDX-FP 1J1000T6')
    # sensor type: Force
    gdx.select_sensors(1)
    # sample rate: 1ms
    gdx.start(1)
    column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
    logger.info('\n')
    logger.info(column_headers)

    databuffer = []
    count = 0
    try:
        while True:
            measurements = gdx.read()
            if measurements == None:
                break
            count = count + 1
            ts = current_milli_time()
            # logger.info(f"count:{count} ts:{ts} measurements:{measurements[0]}")
            newdata = ["deviceid",count,measurements[0],ts]
            databuffer.append(newdata)
            if (count > 1 and count % 1000 == 0):
                p = Process(target=func, args=(databuffer))
                p.start()
                # pass_buf_to_server(databuffer)
                databuffer = []
    except KeyboardInterrupt:
        pass

    gdx.stop()
    gdx.close()

# input("Press Enter to exit...")
