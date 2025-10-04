from datetime import datetime
from random import randint
from uuid import UUID
from pydantic import BaseModel,Field
from app.database.models import ShipmentStatus

def location():
        return randint(11000,12000)


class BaseShipment(BaseModel):
        content: str
        weight: float = Field(le=25,ge=1)
        destination: int | None = Field(default_factory=location,description="Random Destination if not set")
        

class ShipmentRead(BaseShipment):
        id: UUID
        status: ShipmentStatus
        estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
       pass

class ShipmentPatch(BaseModel):
        status: ShipmentStatus | None = Field(default=None)
        estimated_delivery: datetime | None = Field(default=None)
        