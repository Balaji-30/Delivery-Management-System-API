

from pydantic import BaseModel, EmailStr, Field

class BaseSeller(BaseModel):
    name: str
    email: EmailStr

class SellerRead(BaseSeller):
    pass

class SellerCreate(BaseSeller):
    password: str
    address: str | None =Field(default=None)
    zipcode: int | None=Field(default=None)