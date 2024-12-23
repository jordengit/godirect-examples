import logging
import logging.config
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import pprint
from pydantic import BaseModel
import json
from datetime import datetime
import queue

# setup loggers
logging.config.fileConfig('apiserver.logconfig', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)  # the __name__ resolve to "main" since we are at the root of the project.
                                      # This will get the root logger since no logger in the configuration has this name.

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

databuffer_lock = asyncio.Lock()
databuffer = []

q = queue.Queue()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/dump/{start}/to/{end}")
async def dump(start: int, end: int):
# async def dump():
    # global databuffer
    ret = ""
    # async with databuffer_lock:
    #     for row in databuffer:
    #         logger.info(f"deviceid:{row[0]} cnt:{row[1]} data:{row[2]} ts:{row[3]}")
    #     ret = pprint.pformat(databuffer)
    #     databuffer = []
    databuffer = []
    while not q.empty():
        item = q.get()
        if (item[3] >= start and item[3] <= end):
            databuffer.append(item)
        # if (item[3] > end):
        #     break

    ret = pprint.pformat(databuffer)
    return ret

@app.get("/add/{deviceid}/data/{data}/cnt/{cnt}/ts/{ts}")
async def add(deviceid: str,data: float,cnt: int,ts: int):
    # global counter
    # global databuffer
    newdata = [deviceid,cnt,data,ts]
    # async with counter_lock:
    #     counter += 1
    # async with databuffer_lock:
    #     databuffer.append(newdata)
    q.put(newdata)
    # logger.info(f"no:{counter} cnt:{cnt} data:{data} ts:{ts}")
    return "OK"

class PlateData(BaseModel):
    data: list = []

@app.post("/addbuf/")
async def addbuf(buf: PlateData):
    logger.info(f"buf len: {len(buf.data)}")
    # begin = buf.data[0][3]
    # end = buf.data[999][3]
    # dt_begin = datetime.fromtimestamp(begin)
    # dt_end = datetime.fromtimestamp(end)
    # logger.info(f"begin: {dt_begin}")
    # logger.info(f"end: {dt_end}")
    # async with databuffer_lock:
        # databuffer.append(row)
        # logger.info(f"deviceid:{row[0]} cnt:{row[1]} data:{row[2]} ts:{row[3]}")
    for row in buf.data:
        q.put(row)
    return "OK"

# python -m venv env
# uvicorn demo:app --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem --host 0.0.0.0 --port 8000 --workers=2
# fastapi dev demo.py
# GDX-FP 1J1000T6
# https://philstories.medium.com/fastapi-logging-f6237b84ea64
# uvicorn demo:app --host 0.0.0.0 --port 8000
