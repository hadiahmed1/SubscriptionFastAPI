import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.db.client import db

@pytest_asyncio.fixture
async def async_client():
    await db.connect()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    await db.disconnect()
