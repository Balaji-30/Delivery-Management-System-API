from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)

    async def add(
        self,
        shipment: Shipment,
        location: int = None,
        status: ShipmentStatus = None,
        description: str = None,
    ) -> ShipmentEvent:
        
        if not location or not status:
            last_event=await self.get_latest_event(shipment)
            location = location if location else last_event.location
            status = status if status else last_event.status
            
        new_event=ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(status, location),
            shipment_id=shipment.id
        )

        return await self._add(new_event) 
    
    async def get_latest_event(self,shipment:Shipment):
        
        timeline= shipment.timeline
        timeline.sort(key=lambda x: x.created_at)
        return timeline[-1]
    
    def _generate_description(self, status: ShipmentStatus, location: int) -> str:
        match status:
            case ShipmentStatus.placed:
                return "Assigned to delivery partner, yet to be picked up"
            case ShipmentStatus.out_for_delivery:
                return "Shipment out for delivery"
            case ShipmentStatus.delivered:
                return "Shipment delivered to the customer"
            case ShipmentStatus.cancelled:
                return "Shipment has been cancelled by the seller"
            case _:
                return f"Shipment in transit, last scanned at {location}"