from typing import List

from fastapi import Depends, HTTPException
from app.core.dependancy import get_current_company
from app.db.client import db
from app.schemas.plan_schema import PlanCreate
from prisma.models import Plan,User


async def create_plan(company_id, plan_data: PlanCreate)->Plan:
    feature_connections = [{"id": fid} for fid in plan_data.feature_ids]
    return await db.plan.create(
        data={
            "companyId": company_id,
            "name": plan_data.name,
            "description": plan_data.description,
            "cost": plan_data.cost,
            "discount": plan_data.discount,
            "features": {
                "create": [{"feature": {"connect": {"id": f["id"]}}} for f in feature_connections]
            }
        },
        include={
            "features": True
        }
    )
    
async def find_plans()->List[Plan]:
    return await db.plan.find_many()

async def find_plan_byID(id)->Plan:
    plan=await db.plan.find_unique(where={'id':id})
    if plan is None:
            raise HTTPException(status_code=404, detail="Invalid Plan ID")
