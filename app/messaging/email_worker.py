import asyncio
import json
import smtplib
from email.mime.text import MIMEText
import aio_pika
from app.config import settings

EMAIL_QUEUE = "email_verification_queue"

def send_verification_mail(to_email: str, token: str):
    msg = MIMEText(f"Hesabınızı doğrulamak için: https://senin-domainin.com/verify?token={token}")
    msg["Subject"] = "Hesap doğrulama"
    msg["From"] = settings.gmail_address
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.gmail_address, settings.gmail_app_password)
        server.send_message(msg)

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        send_verification_mail(data["email"], data["verification_token"])
        print(f"Doğrulama maili gönderildi: {data['email']}")

async def main():
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=5)
    queue = await channel.declare_queue(EMAIL_QUEUE, durable=True)
    await queue.consume(on_message)
    print("Email worker dinlemede...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())