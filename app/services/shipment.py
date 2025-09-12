
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.shipment import ShipmentCreate
from app.database.models import Shipment, ShipmentStatus

class ShipmentService:

    def __init__(self,session:AsyncSession):
        self.session=session
        pass
    
    async def get(self,id:int)->Shipment:
        return await self.session.get(Shipment,id)

    async def add(self, shipment_create:ShipmentCreate)->Shipment:
        newShipment = Shipment(
        **shipment_create.model_dump(), 
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
        )
        self.session.add(newShipment)
        await self.session.commit()
        await self.session.refresh(newShipment)
        return newShipment

    async def update(self, shipment_update:dict,id:int)->Shipment:
        shipment = await self.get(id)
        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self,id:int)->None:
        await self.session.delete(await self.get(id))
        await self.session.commit()
