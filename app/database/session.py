from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import Shipment

engine=create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    connect_args={
        "check_same_thread":False
    }

)

def create_db_tables():
    
    SQLModel.metadata.create_all(bind=engine)

def create_session():
    with Session(bind=engine) as session:
        yield session

SessionDep =  Annotated[Session,Depends(create_session)]