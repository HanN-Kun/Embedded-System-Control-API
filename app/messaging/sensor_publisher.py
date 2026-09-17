import json
import aio_pika
from app.messaging.connection import get_channel, declare_sensor_exchange

async def publish_sensor_reading(sensor_id: str, value: float, time_stamp: str):
    channel = await get_channel()
    exchange = await declare_sensor_exchange(channel)

    payload = {
        "sensor_id": sensor_id,
        "value": value,
        "time_stamp": time_stamp,
    }

    await exchange.publish(
        aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key="",
    )