from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, Request, status
from fastapi.templating import Jinja2Templates

from app.api.core.exceptions import NothingToUpdateError
from app.api.dependencies import (
    DeliveryPartnerDep,
    SellerDep,
    SessionDep,
    ShipmentServiceDep,
)
from app.api.schemas.shipment import (
    ShipmentCancel,
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentRead,
)
from app.database.models import Shipment, TagName
from app.utils import TEMPLATE_DIR
from app.config import app_settings

templates = Jinja2Templates(TEMPLATE_DIR)

router = APIRouter(prefix="/shipment", tags=["Shipment"])

# Get shipment details
@router.get("/", response_model=ShipmentRead)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
):
    return await service.get(id)

#Track shipment status page
@router.get("/track", include_in_schema=False)
async def track_shipment(
    request: Request,
    id: UUID,
    service: ShipmentServiceDep,
):
    shipment = await service.get(id)
    context = shipment.model_dump() if shipment else {}
    context["status"] = shipment.status
    context["partner"] = shipment.delivery_partner.name
    context["timeline"] = shipment.timeline
    context["timeline"].reverse()

    return templates.TemplateResponse(
        request=request, name="track.html", context=context
    )

# Submit a new shipment request
@router.post(
    "/submit",
    response_model=ShipmentRead,
    name="Create Shipment",
    description="Submit a new **shipment** request",
    status_code=status.HTTP_201_CREATED,
)
async def submit_shipment(
    seller: SellerDep,
    shipment: ShipmentCreate,
    service: ShipmentServiceDep,
) -> Shipment:
    return await service.add(shipment, seller)

# Update shipment details
@router.patch("/update", response_model=ShipmentRead)
async def shipment_update(
    id: UUID,
    shipmentUpdate: ShipmentUpdate,
    service: ShipmentServiceDep,
    partner: DeliveryPartnerDep,
): 
    update = shipmentUpdate.model_dump(exclude_none=True)
    if not update:
        raise NothingToUpdateError()

    return await service.update(id, shipmentUpdate, partner)

# Add tag to shipment
@router.get("/tag", response_model=ShipmentRead)
async def add_tag_to_shipment(id: UUID, tag: TagName, service: ShipmentServiceDep):
    return await service.add_tag(id, tag)

# Remove tag from shipment
@router.delete("/tag", response_model=ShipmentRead)
async def remove_tag_from_shipment(id: UUID, tag: TagName, service: ShipmentServiceDep):
    return await service.remove_tag(id, tag)

# Get shipments by tag
@router.get("/tagged", response_model=list[ShipmentRead])
async def get_shipments_by_tag(tag_name: TagName, session: SessionDep):
    tag = await tag_name.tag(session)
    return tag.shipments

# Cancel shipment
@router.post("/cancel", response_model=ShipmentRead)
async def cancel_shipment(
    cancellation_info: ShipmentCancel, service: ShipmentServiceDep, seller: SellerDep
):  # pyright: ignore[reportInvalidTypeForm]
    return await service.cancel(**cancellation_info.model_dump(), seller=seller)

# Submit review page
@router.get("/review")
async def submit_review_page(request: Request, token: str):
    return templates.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url": f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
        },
    )

# Submit review
@router.post("/review")
async def submit_review(
    token: str,
    rating: Annotated[int, Form(ge=1, le=5)],
    comment: Annotated[str | None, Form()],
    service: ShipmentServiceDep,
):
    await service.add_review(token, rating=rating, comment=comment)
    return {"detail": "Review submitted successfully"}
