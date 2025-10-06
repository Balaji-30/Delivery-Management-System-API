from uuid import UUID

from fastapi import APIRouter, status, HTTPException

from app.api.dependencies import DeliveryPartnerDep, SellerDep, ShipmentServiceDep
from app.api.schemas.shipment import ShipmentCancel, ShipmentCreate, ShipmentUpdate, ShipmentRead
from app.database.models import Shipment

router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(
    id: UUID,
    service: ShipmentServiceDep,
    _: SellerDep,
):  # pyright: ignore[reportInvalidTypeForm]
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID does not exist"
        )

    return shipment


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
