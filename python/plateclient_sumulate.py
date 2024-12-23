import logging
import logging.config
from gdx import gdx
from time import sleep
import time
import requests
import random
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
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        logger.info(data)
    else:
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

count = 0
databuffer = []

if __name__ == "__main__":
    try:
        while True:
            measurement = random.uniform(16, 17)
            count = count + 1
            ts = current_milli_time()
            # logger.info(f"count:{count} ts:{ts} measurements:{measurement}")
            # pass_data_to_server("1J1000T6", measurement, count, ts)
            newdata = ["deviceid",count,measurement,ts]
            databuffer.append(newdata)
            if (count > 1 and count % 1000 == 0):
                p = Process(target=func, args=(databuffer))
                p.start()
                # p.join()
                # print('done')
                # pass_buf_to_server(databuffer)
                databuffer = []
            time.sleep(1/1000)
    except KeyboardInterrupt:
        pass

# input("Press Enter to exit...")

