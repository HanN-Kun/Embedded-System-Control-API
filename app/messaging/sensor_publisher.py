import json
import aio_pika
from app.messaging.connection import get_channel

SENSOR_QUEUE = "sensor_data_queue"

async def publish_sensor_reading(sensor_id: str, value: float, time_stamp: str):
    channel = await get_channel()
    await channel.declare_queue(SENSOR_QUEUE, durable=True)

    payload = {
        "sensor_id": sensor_id,
        "value": value,
        "time_stamp": time_stamp,
    }

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=SENSOR_QUEUE,
    )