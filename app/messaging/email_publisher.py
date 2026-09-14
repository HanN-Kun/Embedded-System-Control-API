# app/messaging/email_publisher.py
import json
import aio_pika
from app.messaging.connection import get_channel

EMAIL_QUEUE = "email_verification_queue"

async def publish_verification_email(user_id: int, email: str, verification_token: str):
    channel = await get_channel()
    await channel.declare_queue(EMAIL_QUEUE, durable=True)

    payload = {
        "user_id": str(user_id),
        "email": email,
        "verification_token": verification_token,
    }

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=EMAIL_QUEUE,
    )   