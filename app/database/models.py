from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import ARRAY, Column, Integer
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, Relationship, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out for delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class User(SQLModel):
    name: str
    email: EmailStr
    email_verified: bool = Field(default=False)
    password_hash: str


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    customer_email: EmailStr
    customer_phone: str | None = Field(default=None)

    content: str
    weight: float = Field(le=25)
    destination: int
    estimated_delivery: datetime

    timeline: list["ShipmentEvent"] = Relationship(
        back_populates="shipment", sa_relationship_kwargs={"lazy": "selectin"}
    )

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    review: "Review"= Relationship(back_populates="shipment",sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def status(self):
        return self.timeline[-1].status if len(self.timeline) > 0 else None


class ShipmentEvent(SQLModel, table=True):
    __tablename__ = "shipment_event"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )
    location: int
    status: ShipmentStatus
    description: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment = Relationship(
        back_populates="timeline", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Seller(User, table=True):
    __tablename__ = "seller"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP, default=datetime.now)
    )

    address: str | None = Field(default=None)
    zipcode: int | None = Field(default=None)

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )


class DeliveryPartner(User, table=True):
    __tablename__ = "delivery_partner"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )
    serviceable_zipcodes: list[int] = Field(sa_column=Column(ARRAY(Integer)))
    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner", sa_relationship_kwargs={"lazy": "selectin"}
    )

    @property
    def active_shipments(self):
        return [
            shipment
            for shipment in self.shipments
            if shipment.status != ShipmentStatus.delivered
            or shipment.status != ShipmentStatus.cancelled
        ]

    @property
    def current_handling_capacity(self):
        return self.max_handling_capacity - len(self.active_shipments)


class Review(SQLModel, table=True):
    __tablename__="reviews"
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    rating: int = Field(ge=1,le=5)
    comment: str | None = Field(default=None)

    shipment_id: UUID = Field(foreign_key="shipment.id")
    shipment: Shipment= Relationship(
        back_populates="review",
        sa_relationship_kwargs={"lazy":"selectin"}
    )
