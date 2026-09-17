import json
import logging
from app.messaging.connection import get_channel, declare_sensor_exchange, declare_and_bind_queue
from app.websocket.manager import manager

logger = logging.getLogger(__name__)
WS_QUEUE = "sensor_ws_queue"

async def start_sensor_ws_consumer():
    channel = await get_channel()
    exchange = await declare_sensor_exchange(channel)
    queue = await declare_and_bind_queue(channel, exchange, WS_QUEUE)

    async def on_message(message):
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                await manager.broadcast(data)
            except Exception as e:
                logger.error(f"WS broadcast hatası: {e}", exc_info=True)

    await queue.consume(on_message)