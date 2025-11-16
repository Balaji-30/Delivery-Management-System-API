from datetime import timedelta
from uuid import UUID
from fastapi import BackgroundTasks
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.exceptions import BadCredentialsError, ClientNotVerifiedError, InvalidTokenError
from app.database.models import User
from app.services.base import BaseService
from app.services.notification import NotificationService
from app.utils import (
    decode_url_safe_token,
    generate_access_token,
    generate_url_safe_token,
)
from app.config import app_settings
# from app.worker.tasks import send_templated_email

password_context = CryptContext(schemes="bcrypt", deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession, tasks:BackgroundTasks):
        super().__init__(model, session)
        self.notification=NotificationService(tasks)

    async def _add_user(self, data: dict, router_prefix: str):
        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )

        user = await self._add(user)

        token = generate_url_safe_token(
            {
                "email": user.email,
                "id": str(user.id),
            }
        )

        self.notification.send_templated_email(
            recipients=[user.email],
            subject="Verify your email address",
            context={
                "name": user.name,
                "verification_url": f"http://{app_settings.APP_DOMAIN}/{router_prefix}/verify?token={token}",
            },
            template_name="mail_verification.html",
        )

        return user

    async def verify_user_email(self, token: str):
        token_data = decode_url_safe_token(token)

        if not token_data:
            raise InvalidTokenError()

        user = await self._get(UUID(token_data["id"]))
        user.email_verified = True
        await self._update(user)

        pass

    async def _get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )

    async def _generate_token(self, email, password):
        user = await self._get_by_email(email)

        if (
            user is None
            or password_context.verify(password, user.password_hash) is False
        ):
            raise BadCredentialsError()

        if not user.email_verified:
            raise ClientNotVerifiedError()

        return generate_access_token(
            data={"user": {"name": user.name, "id": str(user.id)}}
        )

    async def send_password_reset_link(self, email: EmailStr, router_prefix: str):
        user = await self._get_by_email(email)

        token = generate_url_safe_token({"id": str(user.id)}, salt="password-reset")

        self.notification.send_templated_email(
            recipients=[user.email],
            subject="Shippin Account Password Reset",
            context={
                "name": user.name,
                "reset_url": f"http://{app_settings.APP_DOMAIN}{router_prefix}/reset_password_form?token={token}",
            },
            template_name="mail_password_reset.html",
        )
        


    async def reset_password(self, token: str, password: str)-> bool:
        token_data = decode_url_safe_token(
            token, salt="password-reset", expiry=timedelta(days=1)
        )

        if not token_data:
            return False

        user = await self._get(UUID(token_data["id"]))
        user.password_hash = password_context.hash(password)

        await self._update(user)
        return True

