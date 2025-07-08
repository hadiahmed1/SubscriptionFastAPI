from typing import List
from fastapi import Depends, HTTPException, Request
from app.core.dependancy import get_current_user
from app.db.client import db
from app.schemas.plan_schema import PlanCreate
from prisma.models import Plan


async def validate_feature_ids_for_company(feature_ids: list[str], company_id: str):
    company_features = await db.feature.find_many(where={"companyId": company_id})
    valid_feature_ids = {f.id for f in company_features}

    invalid_ids = [fid for fid in feature_ids if fid not in valid_feature_ids]
    if invalid_ids:
        raise HTTPException(
            status_code=400, detail=f"Invalid feature IDs for company: {invalid_ids}"
        )


async def create_plan(company_id, plan_data: PlanCreate) -> Plan:
    feature_connections = [{"id": fid} for fid in plan_data.feature_ids]

    await validate_feature_ids_for_company(plan_data.feature_ids, company_id)

    # razorpay_plan_id = create_razor_pay_plan(name=plan_data.name, amount=plan_data.cost)

    # plan = razorpay_client.plan.create(
    #     {
    #         "period": "monthly",
    #         "interval": 1,
    #         "item": {
    #             "name": "Basic Monthly Plan",
    #             "amount": 99900,
    #             "currency": "INR",
    #             "description": "Monthly subscription",
    #         },
    #     }
    # )
    return await db.plan.create(
        data={
            "companyId": company_id,
            # "": razorpay_plan_id,
            # "rzp_planId": plan.id,
            "name": plan_data.name,
            "description": plan_data.description,
            "cost": plan_data.cost,
            "discount": plan_data.discount,
            "validity": plan_data.validity,
            "features": {
                "create": [
                    {"feature": {"connect": {"id": f["id"]}}}
                    for f in feature_connections
                ]
            },
        },
        include={"features": True},
    )


async def find_plans(where={}) -> List[Plan]:
    return await db.plan.find_many(
        where=where,
        include={
            "company": True,
            "features": {"include": {"feature": True}},
        },
    )


async def find_my_plans(request: Request) -> List[Plan]:
    try:
        user = await get_current_user(request=request)
        # finding suscribed plans
        subscriptions = await db.subscription.find_many(where={"subscriberId": user.id})
        subscribed_plan_ids = [sub.planId for sub in subscriptions]

        return await find_plans(where={"id": {"not_in": subscribed_plan_ids}})
    except HTTPException:
        return await find_plans()


async def find_plan_byID(id) -> Plan:
    plan = await db.plan.find_unique(
        where={"id": id},
        include={
            "company": True,
            "features": {"include": {"feature": True}},
        },
    )
    if plan is None:
        raise HTTPException(status_code=404, detail="Invalid Plan ID")
    return plan
