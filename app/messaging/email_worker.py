import asyncio
import json
import smtplib
from email.mime.text import MIMEText
import aio_pika
from app.config import settings
import logging
from app.core.logging_config import setup_logging
from app.core.sentry_setup import init_sentry

init_sentry()

logger = logging.getLogger(__name__)

EMAIL_QUEUE = "email_verification_queue"

def send_verification_mail(to_email: str, token: str):
    msg = MIMEText(f"Hesabınızı doğrulamak için: http://127.0.0.1:8000/users/verify?token={token}")
    msg["Subject"] = "Hesap doğrulama"
    msg["From"] = settings.gmail_address
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.gmail_address, settings.gmail_app_password)
        server.send_message(msg)

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            send_verification_mail(data["email"], data["verification_token"])
            print(f"Doğrulama maili gönderildi: {data['email']}")
        except Exception as e:
            logger.error(f"Doğrulama maili gönderilemedi: {e}", exc_info=True)

async def main():
    setup_logging()

    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=5)
    queue = await channel.declare_queue(EMAIL_QUEUE, durable=True)
    await queue.consume(on_message)
    print("Email worker dinlemede...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())