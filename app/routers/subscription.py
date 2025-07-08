from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependancy import get_current_user
from prisma.models import User, Subscription
from prisma.errors import UniqueViolationError
from app.services.suscription_service import get_my_subscriptions, suscribe

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.post("/{plan_id}", status_code=status.HTTP_201_CREATED)
async def post_subscription(
    plan_id, user: User = Depends(get_current_user)
) -> Subscription:
    try:
        new_subscription = await suscribe(user.id, planId=plan_id)
        return new_subscription
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subscription already exists for this company.",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_subscriptions(
    user: User = Depends(get_current_user),
) -> List[Subscription]:
    return await get_my_subscriptions(user.id)
