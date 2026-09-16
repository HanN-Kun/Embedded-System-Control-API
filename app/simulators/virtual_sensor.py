import asyncio
import random
from datetime import datetime, timezone
from app.messaging.sensor_publisher import publish_sensor_reading
from app.config import settings

async def run():
    if not settings.virtual_sensor_id:
        raise RuntimeError("VIRTUAL_SENSOR_ID .env dosyasında tanımlı değil")

    while True:
        value = round(random.uniform(18.0, 30.0), 2)
        time_stamp = datetime.now(timezone.utc).isoformat()

        await publish_sensor_reading(settings.virtual_sensor_id, value, time_stamp)
        print(f"Sahte veri gönderildi: sensor_id={settings.virtual_sensor_id}, value={value}", flush=True)

        await asyncio.sleep(settings.virtual_sensor_interval_seconds)

if __name__ == "__main__":
    asyncio.run(run())