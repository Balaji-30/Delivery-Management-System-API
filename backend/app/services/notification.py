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

    def send_email(
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

    def send_templated_email(
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

    def send_sms(self, to: str, body: str):
        
        self.tasks.add_task(
            self.twilio_client.messages.create_async, 
            from_=notifications_settings.TWILIO_NUMBER,
            to=to,
            body=body,
        )
    
    def add_log(self, message: str):
        """
        Schedules a log message to be printed to the console.
        Render (or any cloud host) will capture this in its log stream.
        """
        self.tasks.add_task(
            print,                   # 1. The function to run
            f"[APP_LOG]: {message}"   # 2. The argument for that function
        )