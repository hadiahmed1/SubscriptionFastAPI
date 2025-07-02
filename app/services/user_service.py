from fastapi import HTTPException
from app.core.security import verify_password
from prisma.models import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.db.client import db


async def get_user(identifier: str) -> User:
    user = await db.user.find_first(
        where={
            "OR": [
                {"username": identifier},
                {"email": identifier},
            ]
        }
    )
    return user


async def authenticate_user(identifier: str, password: str):
    user: User | None = await get_user(identifier)

    if user is None or not verify_password(password, user.password):
        return False
    return user


async def create_user(user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)

    return await db.user.create(
        data={
            "username": user_data.username,
            "email": user_data.email,
            "role": user_data.role,
            "password": hashed_password,
        }
    )


async def get_company(company_id):
    company = await db.user.find_unique(where={"id": company_id, "role": "COMPANY"})
    if company is None:
        raise HTTPException(
            status_code=400,
            detail="Feature with this name already exists for this company.",
        )
    else:
        return company
