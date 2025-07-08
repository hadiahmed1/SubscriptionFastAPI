import pytest
from app.core.config import ALGORITHM
from jose import jwt


# SUCCESSFUL LOGIN
@pytest.mark.asyncio
async def test_post_token_success(async_client):
    response = await async_client.post(
        "/auth/token", json={"username": "hadi", "password": "hadi"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "hadi"
    assert data["user"]["role"] == "USER"
    assert "access_token" in response.cookies


# COMPANY LOGIN
@pytest.mark.asyncio
async def test_company_post_token_success(async_client):
    response = await async_client.post(
        "/auth/token", json={"username": "comp1", "password": "comp1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "comp1"
    assert data["user"]["role"] == "COMPANY"
    assert "access_token" in response.cookies


# WRONG PASSWORD
@pytest.mark.asyncio
async def test_post_token_wrong_password(async_client):
    response = await async_client.post(
        "/auth/token", json={"username": "hadi", "password": "hadiahmed"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


# INVALID USER
@pytest.mark.asyncio
async def test_post_token_wrong_username(async_client):
    response = await async_client.post(
        "/auth/token", json={"username": "hadia", "password": "hadiahmed"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


# GET USER SUCCESSFULLY WITH COOKIES
@pytest.mark.asyncio
async def test_get_user_success(async_client):
    # getting access token
    response = await async_client.post(
        "/auth/token", json={"username": "hadi", "password": "hadi"}
    )
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]

    # accessing protected route /users/me
    response = await async_client.get(
        "/users/me", cookies={"access_token": access_token}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "hadi"


# GET USER FAIL WITHOUT COOKIES
@pytest.mark.asyncio
async def test_get_user_fail_without_cookie(async_client):
    response = await async_client.get("/users/me")

    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Please Login"


# GET USER FAIL WITH INVALID TOKEN
@pytest.mark.asyncio
async def test_get_user_fail_with_invlaid_token(async_client):

    to_encode = data = {"id": "ksdhfaksjhf", "role": "USER"}
    access_token = jwt.encode(to_encode, "wrong-key", algorithm=ALGORITHM)
    response = await async_client.get(
        "/users/me", cookies={"access_token": access_token}
    )

    data = response.json()
    print(data)
    assert response.status_code == 401
    assert data["detail"] == "Invalid token"
