from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from app.api.core.exceptions import InvalidTokenError
from app.api.core.security import TokenData
from app.api.dependencies import SellerDep, SellerServiceDep, get_seller_access_token
from app.api.schemas.seller import SellerCreate, SellerRead
from app.api.schemas.shipment import ShipmentRead
from app.config import app_settings
from app.database.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix="/seller", tags=["Seller"])


@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)


@router.get("/verify")
async def verify_seller(token: str, service: SellerServiceDep):
    try:
        await service.verify_user_email(token)
        return RedirectResponse(url=f"https://{app_settings.APP_DOMAIN}/seller/login?verified=true")
    except (InvalidTokenError,Exception):
        return RedirectResponse(url=f"https://{app_settings.APP_DOMAIN}/seller/login?verified=false")


@router.get("/forgot_password")
async def seller_forgot_password(email: EmailStr, service: SellerServiceDep):
    await service.send_password_reset_link(email, router.prefix)
    return {"detail": "Please check your email for the password reset link."}


@router.get("/reset_password_form")
async def get_seller_reset_password_form(request: Request, token: str):
    templates = Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password_reset_form.html",
        context={
            "reset_url": f"http://{app_settings.APP_DOMAIN}{router.prefix}/reset_password?token={token}"
        },
    )

@router.post("/reset_password")
async def reset_seller_password(
    request: Request,
    token: str,
    password: Annotated[str,Form()],
    service: SellerServiceDep,
):
    is_success = await service.reset_password(token, password)

    templates= Jinja2Templates(TEMPLATE_DIR)

    return templates.TemplateResponse(
        request=request,
        name="password/password_reset_successful.html" if is_success else "password/password_reset_unsuccessful.html"
    )


@router.post("/login", response_model=TokenData)
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.login(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "jwt"}


# Logout the seller by blacklisting the token
@router.get("/logout")
async def logout_seller(
    token_data: Annotated[dict, Depends(get_seller_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"detail": "Successfully logged out"}

# Get logged in seller profile
@router.get("/me", response_model=SellerRead)
async def get_seller_profile(seller:SellerDep):
    return seller

@router.get("/shipments", response_model=list[ShipmentRead])
async def get_seller_shipments(
    seller: SellerDep,
):
    return seller.shipments
    