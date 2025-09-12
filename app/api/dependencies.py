from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import create_session
from app.services.shipment import ShipmentService

SessionDep =  Annotated[AsyncSession,Depends(create_session)]

def get_shipment_service(session: SessionDep):
    return ShipmentService(session)

ServiceDep= Annotated[ShipmentService,Depends(get_shipment_service)]