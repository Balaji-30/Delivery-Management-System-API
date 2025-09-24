from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.security import oauth2_scheme
from app.database.models import Seller
from app.database.session import create_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.utils import decode_access_token

# Async Database session dependency
SessionDep = Annotated[AsyncSession, Depends(create_session)]

# Access token data dependency
def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token"
        )
    return data


# Logged in Seller
async def get_seller(
    token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep
):
    return await session.get(Seller, token_data["user"]["id"])


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(session)


# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)

SellerDep = Annotated[Seller,Depends(get_seller)] 
ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
