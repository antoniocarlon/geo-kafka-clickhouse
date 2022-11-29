import os
import time
import json
import math

import clickhouse_connect

from typing import Union

from fastapi import FastAPI
from kafka import KafkaProducer

KAFKA_HOST = os.getenv('KAFKA_HOST', default='localhost')
KAFKA_PORT = os.getenv('KAFKA_PORT', default=9092)
CLICKHOUSE_HOST = os.getenv('CLICKHOUSE_HOST', default='localhost')

app = FastAPI()
kproducer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
                          value_serializer=lambda v: json.dumps(v).encode('utf-8'))

chclient = clickhouse_connect.get_client(host=CLICKHOUSE_HOST)


@app.get("/put_event")
@app.post("/put_event")
async def put_event(latitude: float,
                    longitude: float,
                    mname: str,
                    mvalue: float,
                    timestamp: Union[int, None] = None):

    message = {
        'timestamp': timestamp if timestamp is not None else int(time.time()),
        'latitude': latitude,
        'longitude': longitude,
        'mname': mname,
        'mvalue': mvalue
    }

    kproducer.send('gkch', message)

    return message


@app.get("/get_aggregation")
async def get_aggregation(polygon: Union[str, None] = None,
                          mname: Union[str, None] = None,
                          timestamp_ini: Union[int, None] = None,
                          timestamp_end: Union[int, None] = None,
                          aggregation: str = 'avg'):

    query = [f"SELECT {aggregation}(mvalue) as mvalue FROM measurements WHERE 1 = 1"]

    if mname is not None:
        query.append(f"mname = '{mname}'")

    if polygon is not None:
        query.append(f"pointInPolygon((longitude, latitude), {polygon})")

    if timestamp_ini is not None:
        query.append(f"timestamp >= {timestamp_ini}")

    if timestamp_end is not None:
        query.append(f"timestamp <= {timestamp_end}")

    result = chclient.query(' AND '.join(query))

    if result and result.result_set and not math.isnan(result.result_set[0][0]):
        return result.result_set[0][0]
    else:
        return None
