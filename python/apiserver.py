import logging
import logging.config
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import numpy as np

# setup loggers
logging.config.fileConfig('apiserver.logconfig', disable_existing_loggers=False)

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

# @app.on_event("startup")
# def startup_event():
#     app.state.data = []

counter_lock = asyncio.Lock()
counter = 0
databuffer_lock = asyncio.Lock()
databuffer = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/dump")
# async def dump(start: int, end: int)
async def dump():
    global databuffer
    async with databuffer_lock:
        for row in databuffer:
            logger.info(f"cnt:{row[0]} data:{row[1]} ts:{row[2]}")
        databuffer = []
    return "OK"

@app.get("/add/{data}/cnt/{cnt}/ts/{ts}")
async def add(data: float,cnt: int,ts: int):
    global counter
    global databuffer
    newdata = [cnt,data,ts]
    async with counter_lock:
        counter += 1
    async with databuffer_lock:
        databuffer.append(newdata)
    # logger.info(f"no:{counter} cnt:{cnt} data:{data} ts:{ts}")
    return "OK"

# python -m venv env
# uvicorn demo:app --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem --host 0.0.0.0 --port 8000 --workers=2
# fastapi dev demo.py
# GDX-FP 1J1000T6
# https://philstories.medium.com/fastapi-logging-f6237b84ea64
# uvicorn demo:app --host 0.0.0.0 --port 8000
