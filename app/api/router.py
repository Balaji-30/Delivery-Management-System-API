from http.client import HTTPException
from typing import Any
from app.api.dependencies import ServiceDep
from app.api.schemas.shipment import ShipmentCreate, ShipmentPatch, ShipmentRead
from app.database.models import Shipment
from fastapi import APIRouter, status


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=ShipmentRead)
async def get_shipment(id: int, service: ServiceDep):  # pyright: ignore[reportInvalidTypeForm]
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID does not exist"
        )

    return shipment


@router.post("/")
async def submit_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:  # pyright: ignore[reportInvalidTypeForm]
    return await service.add(shipment)


@router.patch("/", response_model=ShipmentRead)
async def shipment_update(id: int, shipmentUpdate: ShipmentPatch, service: ServiceDep):  # pyright: ignore[reportInvalidTypeForm]
    update = shipmentUpdate.model_dump(exclude_none=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )
    shipment = await service.update(update, id)
    return shipment


@router.delete("/")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:  # pyright: ignore[reportInvalidTypeForm]
    await service.delete(id)
    return {"detail": f"Shipment #{id} has been deleted!"}
