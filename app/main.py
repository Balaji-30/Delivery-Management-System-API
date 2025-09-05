from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, create_db_tables

from .schema import ShipmentCreate, ShipmentPatch, ShipmentRead


@asynccontextmanager
async def lifespan_handler(app:FastAPI):
        create_db_tables()
        yield
        print("server ended")

app=FastAPI(lifespan=lifespan_handler,servers=[{"url": "http://127.0.0.1:8000", "description": "Local Development Server"}])


@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id: int, session: SessionDep):
        
        shipment=session.get(Shipment,id)
        if shipment is None:
                raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='ID does not exist'
                )
        
        return shipment

@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate,session: SessionDep)-> dict[str,int]:

        newShipment= Shipment( **shipment.model_dump(), status=ShipmentStatus.placed, estimated_delivery=datetime.now() + timedelta(days=3))
        session.add(newShipment)
        session.commit()
        session.refresh(newShipment)
        return {'id':newShipment.id}



@app.patch("/shipment",response_model=ShipmentRead)
def shipment_update(id: int, shipmentUpdate:ShipmentPatch,session:SessionDep):
        
        update=shipmentUpdate.model_dump(exclude_none=True)
        if not update:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No data provided to update"
                )
        shipment=session.get(Shipment,id)
        shipment.sqlmodel_update(update)
        session.add(shipment)
        session.commit()
        session.refresh(shipment)
        
        return shipment

@app.delete("/shipment")
def delete_shipment(id: int,session:SessionDep)-> dict[str,Any]:
        
        session.delete(
                session.get(Shipment,id)
        )
        session.commit()
        return {"detail":f"Shipment #{id} has been deleted!"}
        

@app.get("/scalar",include_in_schema=False)
def get_scalar_docs():
        return get_scalar_api_reference(
                openapi_url=app.openapi_url,
                title="Scalar API"

        )  