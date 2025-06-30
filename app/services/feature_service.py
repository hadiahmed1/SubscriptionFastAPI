from typing import List

from fastapi import HTTPException
from app.db.client import db
from app.schemas.feature_schema import FeatureCreate
from prisma.models import Feature

from app.services.user_service import get_company


async def create_feature(company_id,feature_data: FeatureCreate)->Feature:
    feature = await db.feature.create(data={
        'companyId':company_id,
        'name':feature_data.name,
        'description':feature_data.description,
    })
    return feature
    
async def find_features(companyId)->List[Feature]:
    company = await get_company(company_id=companyId)
    return await db.feature.find_many(where={"companyId":company.id})

async def find_feature_byID(id)->Feature:
    feature = await db.feature.find_unique(where={'id':id})
    if feature is None:
            raise HTTPException(status_code=404, detail="Invalid Feature ID")