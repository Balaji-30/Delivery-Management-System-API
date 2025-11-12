from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.config import database_settings

engine=create_async_engine(
    url=database_settings.POSTGRES_URL ,
    echo=True
)

async def create_db_tables():
    async with engine.begin() as conn:
        from app.database.models import Shipment,Seller # Import models here to ensure they are registered before creating tables  # noqa: F401
        await conn.run_sync(SQLModel.metadata.create_all)

async def create_session():
    async_session= sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

