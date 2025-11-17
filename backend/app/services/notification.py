from fastapi import BackgroundTasks
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import notifications_settings
from app.utils import TEMPLATE_DIR

from twilio.rest import Client
from jinja2 import Environment, FileSystemLoader, select_autoescape

import resend


class NotificationService:
    def __init__(self, tasks: BackgroundTasks):
        self.tasks = tasks
        # self.fastmail = FastMail(
        #     ConnectionConfig(
        #         **notifications_settings.model_dump(
        #             exclude=["TWILIO_SID", "TWILIO_AUTH_TOKEN", "TWILIO_NUMBER"]
        #         ),
        #         TEMPLATE_FOLDER=TEMPLATE_DIR,
        #     )
        # )
        self.template_env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            autoescape=select_autoescape(['html', 'xml'])
        )

        resend.api_key = notifications_settings.RESEND_API_KEY

        self.twilio_client = Client(
            notifications_settings.TWILIO_SID, notifications_settings.TWILIO_AUTH_TOKEN
        )

    # def send_email(
    #     self,
    #     recipients: list[EmailStr],
    #     subject: str,
    #     body: str,
    # ):
    #     self.tasks.add_task(
    #         self.fastmail.send_message,
    #         message=MessageSchema(
    #             recipients=recipients,
    #             subject=subject,
    #             body=body,
    #             subtype=MessageType.plain,
    #         ),
    #     )

    def _send_resend_task(self, recipients: list[str], subject: str, html: str = None, text: str = None):
        """
        Internal helper to perform the synchronous Resend API call.
        This runs in a thread pool via BackgroundTasks.
        """
        try:
            email_data = {
                "from": "Shippin Support <noreply@shippin.me>", # CHANGE THIS to your verified domain later
                "to": recipients,
                "subject": subject,
            }
            
            if html:
                email_data["html"] = html
            if text:
                email_data["text"] = text

            r = resend.Emails.send(email_data)
            print(f"[Email Sent]: ID {r.get('id')}")
            
        except Exception as e:
            print(f"[Email Failed]: {e}")

    def send_templated_email(
        self,
        recipients: list[EmailStr],
        subject: str,
        context: dict,
        template_name: str,
    ):
        # self.tasks.add_task(
        #     self.fastmail.send_message,
        #     message=MessageSchema(
        #         recipients=recipients,
        #         subject=subject,
        #         template_body=context,
        #         subtype=MessageType.html,
        #     ),
        #     template_name=template_name,
        # )
        try:
            template = self.template_env.get_template(template_name)
            html_content = template.render(**context)
            
            recipient_strs = [str(r) for r in recipients]

            # 2. Add the sending task to background
            self.tasks.add_task(
                self._send_resend_task,
                recipients=recipient_strs,
                subject=subject,
                html=html_content
            )
        except Exception as e:
            print(f"Error rendering template: {e}")

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