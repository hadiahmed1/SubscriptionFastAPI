from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from app.db.client import db
from app.services.plan_service import find_plan_byID

include_conditions = {
    "plan": {"include": {"company": True, "features": {"include": {"feature": True}}}}
}


async def suscribe(userId, planId):
    plan = await find_plan_byID(planId)
    old_sub = await db.subscription.find_unique(
        where={"subscriberId_planId": {"subscriberId": userId, "planId": planId}}
    )
    if old_sub:
        raise HTTPException(
            status_code=403, detail="User is already subscribed to this plan."
        )
    return await db.subscription.create(
        data={
            "planId": plan.id,
            "subscriberId": userId,
            "expiresOn": datetime.now(timezone.utc) + timedelta(days=plan.validity),
        },
        include=include_conditions,
    )


async def get_my_subscriptions(userId):
    return await db.subscription.find_many(
        where={"subscriberId": userId},
        include=include_conditions,
    )
