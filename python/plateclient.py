import logging
import logging.config
from gdx import gdx
from time import sleep
import time
import requests

# setup loggers
logging.config.fileConfig('plateclient.logconfig', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.
def pass_data_to_server(data, cnt, ts):

    # Define the API endpoint
    api_url = f"http://127.0.0.1:8000/add/{data}/cnt/{cnt}/ts/{ts}"
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

def current_milli_time():
    return round(time.time() * 1000)

gdx = gdx.gdx()
gdx.open(connection='ble',device_to_open='GDX-FP 1J1000T6')
# sensor type: Force
gdx.select_sensors([1])
# sample rate: 1ms
gdx.start(1)
column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
logger.info('\n')
logger.info(column_headers)

count = 0
try:
    while True:
        measurements = gdx.read()
        if measurements == None:
            break
        count = count + 1
        ts = current_milli_time()
        logger.info(f"count:{count} ts:{ts} measurements:{measurements[0]}")
        pass_data_to_server(measurements[0], count, ts)
except KeyboardInterrupt:
    pass

gdx.stop()
gdx.close()

input("Press Enter to exit...")
