from pydantic import BaseModel, ConfigDict, EmailStr, Field

class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zipcodes: list[int]
    max_handling_capacity: int

    model_config = ConfigDict(from_attributes=True)

class DeliveryPartnerRead(BaseDeliveryPartner):
    pass

class DeliveryPartnerUpdate(BaseModel):
    serviceable_zipcodes: list[int] | None = Field(default=None)
    max_handling_capacity: int | None = Field(default=None)

class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str