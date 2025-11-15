from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.core.exceptions import NothingToUpdateError
from app.api.core.security import TokenData
from app.api.dependencies import (
    DeliveryPartnerDep,
    DeliveryPartnerServiceDep,
    get_partner_access_token,
)
from app.api.schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from app.api.schemas.shipment import ShipmentRead
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR
from app.config import app_settings

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
    partner: DeliveryPartnerCreate,
    service: DeliveryPartnerServiceDep,
):
    return await service.add(partner)

@router.get("/verify")
async def verify_delivery_partner(token:str,service:DeliveryPartnerServiceDep):
    
    await service.verify_user_email(token)
    return {"detail":"Account Verified"}


@router.post("/login", response_model=TokenData)
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


# Update the delivery partner details
@router.post("/update", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    update = partner_update.model_dump(exclude_none=True)
    if not update:
        raise NothingToUpdateError()
    return await service.update(partner.sqlmodel_update(update))


# Logout the delivery partner by blacklisting the token
@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}

@router.get("/forgot_password")
async def delivery_partner_forgot_password(email: EmailStr, service: DeliveryPartnerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Please check your email for the password reset link."}


@router.get("/reset_password_form")
async def get_delivery_partner_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password_reset_form.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )


@router.post("/reset_password")
async def reset_delivery_partner_password(
    request: Request,
    token: str,
    password: Annotated[str,Form()],
    service: DeliveryPartnerServiceDep,
):
    is_success = await service.reset_password(token, password)

    templates= Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/password_reset_successful.html" if is_success else "password/password_reset_unsuccessful.html"
    )

# Get logged in deliver partner profile
@router.get("/me", response_model=DeliveryPartnerRead)
async def get_partner_profile(partner: DeliveryPartnerDep):
    return partner

@router.get("/shipments", response_model=list[ShipmentRead])
async def get_shipments(
    partner: DeliveryPartnerDep,
):
    return partner.shipments