from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlmodel import SQLModel
from app.database.session import create_session
from app.main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.tests import example

engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
test_session = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def create_session_override():
    async with test_session() as session:
        yield session

@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://testserver",
    ) as client:
        yield client

@pytest_asyncio.fixture(scope="session")
async def seller_token(client: AsyncClient):
    response = await client.post(
        "/seller/login",
        data={
            "grant_type":"password",
            "username":example.SELLER["email"],
            "password":example.SELLER["password"],
        }
    )

    assert "access_token" in response.json()
    return response.json()["access_token"]
    

@pytest_asyncio.fixture(scope="session",autouse=True)
async def setup_and_teardown():
    print("Starting Tests...\n")

    app.dependency_overrides[create_session]= create_session_override

    async with engine.begin() as conn:
        from app.database.models import Shipment,Seller,DeliveryPartner # noqa: F401
        await conn.run_sync(SQLModel.metadata.create_all)
    
    async with test_session() as session:
        await example.create_test_data(session)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    app.dependency_overrides.clear()
    print("\nTests Completed.")