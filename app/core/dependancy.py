from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from app.db.client import db
from prisma.models import User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.user.find_unique(where={"id": user_id})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

async def get_current_company(user: User = Depends(get_current_user)):
    if user.role != "COMPANY":
        raise HTTPException(status_code=403, detail="Only companies can perform this action")
    return user