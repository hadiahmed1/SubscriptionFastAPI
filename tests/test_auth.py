import pytest

@pytest.mark.asyncio
async def test_post_token(async_client):
    response = await async_client.post(
        "/auth/token", json={"username": "hadi", "password": "hadi"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "hadi"
    assert "access_token" in response.cookies
