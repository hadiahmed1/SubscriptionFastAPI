from typing import List

from fastapi import HTTPException
from app.db.client import db
from app.schemas.plan_schema import PlanCreate
from prisma.models import Plan


async def create_plan(company_id,plan_data: PlanCreate)->Plan:
    return await db.plan.create(data={
        'companyId':company_id,
        'name':plan_data.name,
        'description':plan_data.description,
        'cost':plan_data.cost,
        'discount':plan_data.discount
    })
    
async def find_plans()->List[Plan]:
    return await db.plan.find_many()

async def find_plan_byID(id):
    plan=await db.plan.find_unique(where={'id':id})
    if plan is None:
            raise HTTPException(status_code=404, detail="Invalid Plan ID")
