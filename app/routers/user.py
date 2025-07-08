from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreate
from app.services.user_service import create_user
from prisma.errors import UniqueViolationError

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    try:
        new_user = await create_user(user)
        # new_user.password = None
        return new_user
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists.",
        )
