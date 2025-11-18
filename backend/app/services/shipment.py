from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.core.exceptions import ClientNotAuthorizedError, EntityNotFoundError, InvalidTokenError
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate
from app.database.models import DeliveryPartner, Review, Seller, Shipment, ShipmentStatus, TagName
from app.database.redis import get_shipment_verification_code
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService
# from app.services.notification import NotificationService
from app.services.shipment_event import ShipmentEventService
from app.utils import decode_url_safe_token


class ShipmentService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        partner_service: DeliveryPartnerService,
        event_service: ShipmentEventService,
    ):
        super().__init__(Shipment, session)
        self.partner_service = partner_service
        self.event_service = event_service
        # self.notification=notification

    async def get(self, id: UUID) -> Shipment | None:
        shipment = await self._get(id)

        if not shipment:
            raise EntityNotFoundError()
        return shipment

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)

        event = await self.event_service.add(
            shipment=shipment,
            location=seller.zipcode if seller.zipcode else 000000,
            status=ShipmentStatus.placed,
            description=f"Shipment assigned to {partner.name}",
        )

        shipment.timeline.append(event)
        return shipment

    async def update(
        self,
        id: UUID,
        shipment_update: ShipmentUpdate,
        partner: DeliveryPartner,
    ) -> Shipment:
        shipment = await self.get(id)

        if shipment.delivery_partner_id != partner.id:
            raise ClientNotAuthorizedError()

        if shipment_update.status == ShipmentStatus.delivered:
            code = await get_shipment_verification_code(shipment.id)
            if int(code) != shipment_update.verification_code:
                raise ClientNotAuthorizedError()

        update_data = shipment_update.model_dump(
            exclude_none=True,
            exclude=[
                "verification_code",
            ],
        )

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        if len(update_data) > 1 or not shipment_update.estimated_delivery:
            await self.event_service.add(
                shipment=shipment,
                **update_data,
            )

        shipment.sqlmodel_update(update_data)

        return await self._update(shipment)

    async def cancel(self, id: UUID, reason: str | None, seller: Seller) -> Shipment:
        # Validate seller
        shipment = await self.get(id)

        if shipment.seller_id != seller.id:
            raise ClientNotAuthorizedError()

        event = await self.event_service.add(
            shipment=shipment, status=ShipmentStatus.cancelled, description=reason
        )

        shipment.timeline.append(event)
        return shipment

    async def delete(self, id: UUID) -> None:
        await self._delete(await self.get(id))

    async def add_tag(self, id:UUID, tag_name:TagName)->None:
        shipment = await self.get(id)
        shipment.tags.append(await tag_name.tag(self.session))
        return await self._update(shipment)
    
    async def remove_tag(self, id:UUID, tag_name:TagName)->None:
        shipment = await self.get(id)
        try:
            shipment.tags.remove(await tag_name.tag(self.session))
        except ValueError:
            raise EntityNotFoundError
        return await self._update(shipment)



    async def add_review(self, token: str, rating: int, comment: str) -> None:

        token_data = decode_url_safe_token(token)

        if not token_data:
            raise InvalidTokenError()
        shipment= await self._get(UUID(token_data["id"]))

        new_review = Review(
            rating=rating,
            comment=comment if comment else None,
            shipment_id=shipment.id,
        )

        self.session.add(new_review)
        await self.session.commit()


