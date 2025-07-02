from datetime import datetime, timedelta
from app.db.client import db
from app.services.plan_service import find_plan_byID

include_conditions = {
    "plan": {"include": {"company": True, "features": {"include": {"feature": True}}}}
}


async def suscribe(userId, planId):
    plan = await find_plan_byID(planId)
    return await db.subscription.create(
        data={
            "planId": plan.id,
            "subscriberId": userId,
            "expiresOn": datetime.utcnow() + timedelta(days=30),
        },
        include=include_conditions,
    )


async def get_my_subscriptions(userId):
    return await db.subscription.find_many(
        where={"subscriberId": userId},
        include=include_conditions,
    )
