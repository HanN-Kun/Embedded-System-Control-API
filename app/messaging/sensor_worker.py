import asyncio
import json
import uuid
from datetime import datetime
import aio_pika
from app.config import settings
from app.database import SessionLocal
from app.models.sensor_reading import SensorReading
from app.repositories import sensor_reading_repository, sensor_repository
import logging
from app.core.logging_config import setup_logging
from app.core.sentry_setup import init_sentry

init_sentry()

logger = logging.getLogger(__name__)

SENSOR_QUEUE = "sensor_data_queue"

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        db = SessionLocal()
        try:
            sensor_id = uuid.UUID(data["sensor_id"])
            sensor = sensor_repository.get_by_id(db, sensor_id)
            if not sensor:
                logger.error(f"Bilinmeyen sensor_id ile veri geldi, atlanıyor: {sensor_id}")
                return

            reading = SensorReading(
                sensor_id=sensor_id,
                value=data["value"],
                time_stamp=datetime.fromisoformat(data["time_stamp"]),
            )
            sensor_reading_repository.create(db, reading)
            print(f"Sensor verisi DB'ye yazıldı: {data['sensor_id']} -> {data['value']}", flush=True)
        except Exception as e:
            logger.error(f"Sensor verisi işlenemedi: {e}", exc_info=True)
        finally:
            db.close()

async def main():
    setup_logging()

    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=5)
    queue = await channel.declare_queue(SENSOR_QUEUE, durable=True)
    await queue.consume(on_message)
    print("Sensor worker dinlemede...", flush=True)
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())