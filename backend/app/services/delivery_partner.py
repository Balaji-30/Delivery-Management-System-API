from sqlmodel import Sequence, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.core.exceptions import DeliveryPartnerNotAvailableError
from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.database.models import DeliveryPartner, Location, Shipment
from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        partner: DeliveryPartner = await self._add_user(
            delivery_partner.model_dump(exclude={"serviceable_zipcodes"}),
            "partner",
        )

        for zipcode in delivery_partner.serviceable_zipcodes:
            location = await self.session.get(Location, zipcode)
            partner.serviceable_locations.append(
                location if location else Location(zip_code=zipcode)
            )

        return await self._update(partner)

    async def get_partners_by_zipcode(self, zipcode: str) -> Sequence[DeliveryPartner]:
        return (
            await self.session.scalars(
                select(DeliveryPartner)
                .join(DeliveryPartner.serviceable_locations)
                .where((Location.zip_code == int(zipcode)))
            )
        ).all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partners_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        raise DeliveryPartnerNotAvailableError()

    async def update(self, partner: DeliveryPartner) -> DeliveryPartner:
        return await self._update(partner)

    async def login(self, email: str, password: str) -> str:
        return await self._generate_token(email, password)
