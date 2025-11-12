from typing import Annotated
from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.exceptions import ClientNotAuthorizedError, InvalidTokenError
from app.api.core.security import oauth2_scheme_partner, oauth2_scheme_seller
from app.database.models import DeliveryPartner, Seller
from app.database.redis import is_jti_blacklisted
from app.database.session import create_session
from app.services.delivery_partner import DeliveryPartnerService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from app.services.shipment_event import ShipmentEventService
from app.utils import decode_access_token

# Async Database session dependency
SessionDep = Annotated[AsyncSession, Depends(create_session)]


# Access token data dependency
async def _get_access_token(token: str) -> dict:
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise InvalidTokenError()
    return data


async def get_seller_access_token(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
):
    return await _get_access_token(token)


async def get_partner_access_token(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
):
    return await _get_access_token(token)


# Logged in Seller
async def get_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
    session: SessionDep,
):
    seller = await session.get(Seller, UUID(token_data["user"]["id"]))

    if seller is None:
        raise ClientNotAuthorizedError()

    return seller


async def get_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
    session: SessionDep,
):
    partner = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))

    if partner is None:
        raise ClientNotAuthorizedError()

    return partner


# Shipment service dep
def get_shipment_service(session: SessionDep):
    return ShipmentService(
        session,
        DeliveryPartnerService(session),
        ShipmentEventService(session),

    )


# Seller service dep
def get_seller_service(session: SessionDep):
    return SellerService(session)


def get_delivery_partner_service(session: SessionDep):
    return DeliveryPartnerService(session)


SellerDep = Annotated[Seller, Depends(get_seller)]
DeliveryPartnerDep = Annotated[DeliveryPartner, Depends(get_partner)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
DeliveryPartnerServiceDep = Annotated[
    DeliveryPartnerService, Depends(get_delivery_partner_service)
]
