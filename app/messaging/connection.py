import aio_pika
from app.config import settings

_connection = None

async def get_rabbitmq_connection():
    global _connection
    if _connection is None or _connection.is_closed:
        _connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    return _connection

async def get_channel():
    connection = await get_rabbitmq_connection()
    return await connection.channel()

async def declare_sensor_exchange(channel):
    return await channel.declare_exchange(
        "sensor_exchange", type="fanout", durable=True
    )

async def declare_and_bind_queue(channel, exchange, queue_name: str):
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)
    return queue