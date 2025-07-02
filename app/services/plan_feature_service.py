from fastapi import Depends, HTTPException
from prisma.models import Feature, Plan, PlanFeatures, User
from app.db.client import db
from app.core.dependancy import get_current_company
from app.services.feature_service import find_feature_byID
from app.services.plan_service import find_plan_byID


async def add_plan_feature(
    planId, featureId, company: User = Depends(get_current_company)
) -> PlanFeatures:
    feature: Feature = find_feature_byID(featureId)
    plan: Plan = find_plan_byID(planId)
    if feature.company != company.id or plan.companyId != company.id:
        raise HTTPException(
            status_code=403, detail="Only Plan owner can add Feature to Plan"
        )

    return await db.planfeatures.create(data={"featureId": featureId, "planId": planId})
