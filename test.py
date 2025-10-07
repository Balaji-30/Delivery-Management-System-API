import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config import notifications_settings

fastmail = FastMail(
    ConnectionConfig(
        **notifications_settings.model_dump()
    )
)

async def send_email():
    await fastmail.send_message(
        message= MessageSchema(
            recipients=["ririxo30@gmail.com"],
            subject="Test Email",
            body="This is a test email from FastAPI-Mail",
            subtype=MessageType.plain,
        )
    )
    print("Email sent")

asyncio.run(send_email())