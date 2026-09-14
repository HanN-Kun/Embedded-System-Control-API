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