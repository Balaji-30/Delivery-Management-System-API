from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from twilio.rest import Client

from app.config import database_settings, notifications_settings
from app.utils import TEMPLATE_DIR

fast_mail = FastMail(
    ConnectionConfig(
        **notifications_settings.model_dump(
            exclude=["TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_NUMBER"]
        ),
        TEMPLATE_FOLDER=TEMPLATE_DIR,
    )
)

send_message = async_to_sync(fast_mail.send_message)

twilio_client = Client(
    notifications_settings.TWILIO_SID,
    notifications_settings.TWILIO_AUTH_TOKEN,
)

app = Celery(
    "tasks",
    broker=database_settings.REDIS_URL(db=9),
    backend=database_settings.REDIS_URL(db=9),
    broker_connection_retry_on_startup=True,
)


@app.task
def send_mail(recipients: list[str], subject: str, body: str):
    send_message(MessageSchema(recipients=recipients, subject=subject, body=body))
    return "Mail sent"


@app.task
def send_templated_email(
    recipients: list[EmailStr],
    subject: str,
    context: dict,
    template_name: str,
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )


@app.task
def send_sms(to: str, body: str):
    twilio_client.messages.create(
        from_=notifications_settings.TWILIO_NUMBER,
        to=to,
        body=body,
    )

@app.task
def add_log(message: str)->None:
    with open("file.log","a") as file:
        file.write(f"{message}\n")
