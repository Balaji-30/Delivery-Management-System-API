from pydantic import BaseModel, EmailStr, Field

class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zipcodes: list[int]
    max_handling_capacity: int

class DeliveryPartnerRead(BaseDeliveryPartner):
    pass

class DeliveryPartnerUpdate(BaseModel):
    serviceable_zipcodes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)

class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str