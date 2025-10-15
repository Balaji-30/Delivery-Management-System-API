from app.database.models import Shipment, ShipmentEvent, ShipmentStatus
from app.services.base import BaseService
from app.services.notification import NotificationService


class ShipmentEventService(BaseService):
    def __init__(self, session, tasks):
        super().__init__(ShipmentEvent, session)
        self.notification_service = NotificationService(tasks)

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

        await self._notify(shipment,status)

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
    
    async def _notify(self, shipment:Shipment, status:ShipmentStatus):
        
        if status == ShipmentStatus.in_transit:
            return
        
        subject:str
        context = {}
        template_name:str

        match status:
            case ShipmentStatus.placed:
                subject="Shipment order received!"
                context={
                    "id": shipment.id,
                    "seller": shipment.seller.name,
                    "partner": shipment.delivery_partner.name,
                }
                template_name="mail_placed.html"
                
            case ShipmentStatus.out_for_delivery:
                subject="Your order is out for delivery!"
                context={
                    "partner": shipment.delivery_partner.name,
                }
                template_name="mail_out_for_delivery.html"

            case ShipmentStatus.delivered:
                subject="Your order has been delivered!"
                context={
                    "partner": shipment.delivery_partner.name,
                }
                template_name="mail_delivered.html"
            
            case ShipmentStatus.cancelled:
                subject="Shipment order cancelled"
                context={
                    "seller": shipment.seller.name,
                }
                template_name="mail_cancelled.html"

        await self.notification_service.send_templated_email(
            recipients=[shipment.customer_email],
            subject=subject,
            context=context,
            template_name=template_name,
        )