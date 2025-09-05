from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel


class ShipmentStatus(str,Enum):
        placed="placed"
        in_transit="in transit"
        out_for_delivery="out for delivery"
        delivered="delivered"

class Shipment(SQLModel, table=True):
    __tablename__="shipment"
    id: int = Field(primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
