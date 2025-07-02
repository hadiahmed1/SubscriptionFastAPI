from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.dependancy import get_current_user
from app.schemas.token import Token
from prisma.models import User
from app.services.user_service import authenticate_user
from app.core.auth import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: LoginRequest):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"id": user.id, "role": user.role})

    response = JSONResponse(
        content={
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username, "role": user.role},
        }
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return response

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
