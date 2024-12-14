import logging
from typing import Union
from fastapi import FastAPI
from godirect import GoDirect
from fastapi.middleware.cors import CORSMiddleware
from multiprocessing import Pool, Value
from time import sleep

# setup loggers
logging.config.fileConfig('log.ini', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.
# for i in range(0,20):
#     measurements = gdx.read()
#     if measurements == None:
#         break
#     print(measurements)

# gdx.stop()
# gdx.close()

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    app.state.counter = 0

@app.get("/")
def read_root():
    godirect = GoDirect(use_ble=True)
    device = godirect.get_device(threshold=-100)

    if device != None and device.open(auto_start=False):
            print("connecting.\n")
            print("Connected to "+device.name)
            device.enable_sensors([1])
            device.start(period=10)
            print("start")
            sensors = device.get_enabled_sensors()   # after start() is called, an enabled sensor list is available

            print("Reading measurements\n")
            for i in range(0,10):
                if device.read():
                    for sensor in sensors:
                        # The 'sensor.values' call returns a list of measurements. This list might contain
                        # one sensor value, or multiple sensor values (if fast sampling)
                        print(sensor.sensor_description+": "+str(sensor.values))
                        sensor.clear()
            device.stop()
            device.close()
            print("\nDisconnected from "+device.name)

    else:
            print("Go Direct device not found/opened")

    godirect.quit()


    # global gdx
    # for i in range(0,20):
    #     measurements = gdx.read()
    #     if measurements == None:
    #         break
    #     logger.info(measurements)
    return {"Hello": "World"}

@app.get("/start/{samplerate}")
def start(samplerate: int):
    # global gdx
    # gdx.start(samplerate)
    return "OK"

@app.get("/stop")
def stop():
    # global gdx
    # gdx.stop()
    return "OK"

@app.get("/close")
def close():
    # global gdx
    # gdx.close()
    return "OK"

# python -m venv env
# uvicorn demo:app --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem --host 0.0.0.0 --port 8000 --workers=2
# fastapi dev demo.py
# GDX-FP 1J1000T6
# https://philstories.medium.com/fastapi-logging-f6237b84ea64
# uvicorn demo:app --host 0.0.0.0 --port 8000
