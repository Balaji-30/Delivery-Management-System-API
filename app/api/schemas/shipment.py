from datetime import datetime
from random import randint
from uuid import UUID
from pydantic import BaseModel, EmailStr,Field
from app.database.models import ShipmentEvent, ShipmentStatus

def location():
        return randint(11000,12000)


class BaseShipment(BaseModel):
        content: str
        weight: float = Field(le=25,ge=1)
        destination: int | None = Field(default_factory=location,description="Random Destination if not set")
        

class ShipmentRead(BaseShipment):
        id: UUID
        timeline: list[ShipmentEvent]
        estimated_delivery: datetime


class ShipmentCreate(BaseShipment):
       customer_email: EmailStr
       customer_phone: int | None = Field(default=None)
       pass

class ShipmentUpdate(BaseModel):
        location: int | None = Field(default=None)
        status: ShipmentStatus | None = Field(default=None)
        description: str | None = Field(default=None)
        estimated_delivery: datetime | None = Field(default=None)

class ShipmentCancel(BaseModel):
        id: UUID
        reason: str | None = Field(default=None)
        