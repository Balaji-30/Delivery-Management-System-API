from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.services.base import BaseService
from app.utils import generate_access_token

password_context = CryptContext(schemes="bcrypt", deprecated="auto")

class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        super().__init__(model, session)

    async def _add_user(self, data: dict):

        user = self.model(
            **data,
            password_hash=password_context.hash(data["password"]),
        )
        return await self._add(user)

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller email/password is incorrect",
            )

        return generate_access_token(
            data={"user": {"name": user.name, "id": str(user.id)}}
        )
