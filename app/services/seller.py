from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from app.utils import generate_access_token

password_context = CryptContext(schemes="bcrypt", deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        # Database session to be used in service methods
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        # Logic to add a new seller
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            password_hash=password_context.hash(credentials.password),
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def login(self, email: str, password: str) -> str:
        result = await self.session.execute(select(Seller).where(Seller.email == email))
        seller = result.scalar()

        if seller is None or password_context.verify(password, seller.password_hash) is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller email/password is incorrect",
            )
        
        token = generate_access_token(data={
            "user":
            {
                "name": seller.name,
                "id": seller.id
            }
        })

        return token

        

