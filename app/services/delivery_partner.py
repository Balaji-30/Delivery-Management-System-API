from fastapi import HTTPException,status
from sqlmodel import Sequence, select, any_
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.database.models import DeliveryPartner, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(delivery_partner.model_dump())

    async def get_partners_by_zipcode(self, zipcode: str) -> Sequence[DeliveryPartner]:
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode == any_(DeliveryPartner.serviceable_zipcodes)
                )
            )
        ).all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partners_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        
        raise HTTPException(
            status_code= status.HTTP_406_NOT_ACCEPTABLE,
            detail="No delivery partner available for the shipment",
        )


    async def update(self, partner: DeliveryPartner) -> DeliveryPartner:
        return await self._update(partner)

    async def login(self, email: str, password: str) -> str:
        return await self._generate_token(email, password)
