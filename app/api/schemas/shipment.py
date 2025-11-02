from datetime import datetime
from random import randint
from uuid import UUID
from pydantic import BaseModel, EmailStr,Field
from app.database.models import ShipmentEvent, ShipmentStatus, TagName

def location():
        return randint(11000,12000)


class BaseShipment(BaseModel):
        content: str
        weight: float = Field(le=25,ge=1)
        destination: int | None = Field(default_factory=location,description="Random Destination if not set")

class TagRead(BaseModel):
        name: TagName
        instruction: str
        

class ShipmentRead(BaseShipment):
        id: UUID
        timeline: list[ShipmentEvent]
        estimated_delivery: datetime
        tags: list[TagRead]


class ShipmentCreate(BaseShipment):
       customer_email: EmailStr
       customer_phone: str | None = Field(default=None)


class ShipmentUpdate(BaseModel):
        location: int | None = Field(default=None)
        status: ShipmentStatus | None = Field(default=None)
        verification_code: int | None = Field(default=None)
        description: str | None = Field(default=None)
        estimated_delivery: datetime | None = Field(default=None)

class ShipmentCancel(BaseModel):
        id: UUID
        reason: str | None = Field(default=None)
        
class ShipmentReview(BaseModel):
        rating: int = Field(ge=1,le=5)
        comment: str | None = Field(default=None)
