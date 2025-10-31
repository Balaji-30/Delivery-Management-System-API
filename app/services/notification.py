from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import notifications_settings
from app.utils import TEMPLATE_DIR

from twilio.rest import Client


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        self.fastmail = FastMail(
            ConnectionConfig(
                **notifications_settings.model_dump(
                    exclude=["TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_NUMBER"]
                ),
                TEMPLATE_FOLDER=TEMPLATE_DIR,
            )
        )

        self.twilio_client = Client(
            notifications_settings.TWILIO_SID, notifications_settings.TWILIO_AUTH_TOKEN
        )

    async def send_email(
        self,
        recipients: list[EmailStr],
        subject: str,
        body: str,
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                body=body,
                subtype=MessageType.plain,
            ),
        )

    async def send_templated_email(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):
        self.tasks.add_task(
            self.fastmail.send_message,
            message=MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name,
        )

    async def send_sms(self, to: str, body: str):
        await self.twilio_client.messages.create_async(
            from_=notifications_settings.TWILIO_NUMBER,
            to=to,
            body=body,
        )
