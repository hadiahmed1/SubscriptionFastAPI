import pytest
from app.db.client import db


# CREATE USER
@pytest.mark.asyncio
async def test_create_user(async_client):
    # Creating User
    user_create = {
        "username": "string",
        "email": "user@example.com",
        "role": "USER",
        "password": "string",
    }
    response = await async_client.post("/users/", json=user_create)
    assert response.status_code == 201
    user = response.json()
    assert "id" in user
    assert user["username"] == "string"
    assert user["role"] == "USER"
    assert user["email"] == "user@example.com"
    assert user["password"] != "string"
    # cleanup
    await db.user.delete(where={"username": "string"})


# CREATE DUPLICATE USER
@pytest.mark.asyncio
async def test_create_duplicate_user(async_client):
    # Creating Duplicate User
    user_create = {
        "username": "hadi", #duplicate field
        "email": "user@example.com",
        "role": "USER",
        "password": "string",
    }
    response = await async_client.post("/users/", json=user_create)
    assert response.status_code == 409
    data = response.json()
    assert data["detail"] == "User with this email or username already exists."
