from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from app.main import app
from app.db.client import db

@pytest_asyncio.fixture
async def async_client():
    await db.connect()  # connect Prisma before test
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await db.disconnect()  # disconnect Prisma after test

@pytest.mark.asyncio
async def test_post_token(async_client):
    response = await async_client.post("/auth/token", json={"username": "hadi", "password": "hadi"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "hadi"
    assert "access_token" in response.cookies
