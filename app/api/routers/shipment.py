from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, Request, status, HTTPException
from fastapi.templating import Jinja2Templates

from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCancel, ShipmentCreate, ShipmentUpdate, ShipmentRead
from app.database.models import Shipment
from app.utils import TEMPLATE_DIR
from app.config import app_settings
templates = Jinja2Templates(TEMPLATE_DIR)

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
):  
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID does not exist"
        )

    return shipment

@router.get("/track")
async def track_shipment(
    request: Request,
    id:UUID,
    service: ShipmentServiceDep,
):
    shipment= await service.get(id)
    context= shipment.model_dump() if shipment else {}
    context["status"]= shipment.status
    context["partner"]= shipment.delivery_partner.name
    context["timeline"]= shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request,
        name="track.html",
        context=context
    )



@router.post("/submit", response_model=ShipmentRead)
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
) -> Shipment:  # pyright: ignore[reportInvalidTypeForm]
    return await service.add(shipment, seller)


@router.patch("/update", response_model=ShipmentRead)
async def shipment_update(
    id: UUID,
    shipmentUpdate: ShipmentUpdate,
    service: ShipmentServiceDep,
    partner: DeliveryPartnerDep,
):  # pyright: ignore[reportInvalidTypeForm]

    update = shipmentUpdate.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )
    
    return await service.update(id, shipmentUpdate, partner)
    


@router.post("/cancel", response_model=ShipmentRead)
async def cancel_shipment(cancellation_info: ShipmentCancel, service: ShipmentServiceDep,seller:SellerDep):  # pyright: ignore[reportInvalidTypeForm]
    return await service.cancel(**cancellation_info.model_dump(),seller=seller)

@router.get("/review")
async def submit_review_page(request:Request,token:str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={"review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"},
    )

@router.post("/review")
async def submit_review(token:str, rating:Annotated[int,Form(ge=1,le=5)],comment:Annotated[str | None, Form()], service:ShipmentServiceDep):
    await service.add_review(token,rating=rating,comment=comment)
    return {"detail":"Review submitted successfully"}
