

from httpx import AsyncClient
import pytest
from app.tests import example

base_url = "/shipment/"

@pytest.mark.asyncio
async def test_submit_shipment_auth(client:AsyncClient):
    response = await client.post(
        base_url+"submit",
        json={},
    )

    assert response.status_code == 401
    print(response.json())

@pytest.mark.asyncio
async def test_submit_shipment(client:AsyncClient, seller_token:str):
    response = await client.post(
        base_url+"submit",
        json=example.SHIPMENT,
        headers={"Authorization": f"Bearer {seller_token}"},
    )

    assert response.status_code == 201
    
    response = await client.get(
        base_url,
        params={"id":response.json()["id"]},
    )

    assert response.status_code == 200