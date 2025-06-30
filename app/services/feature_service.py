from typing import List
from app.db.client import db
from app.schemas.feature_schema import FeatureCreate
from prisma.models import Feature

from app.services.user_service import get_company


async def create_feature(company_id,feature_data: FeatureCreate)->Feature:
    return await db.feature.create(data={
        'companyId':company_id,
        'name':feature_data.name,
        'description':feature_data.description,
    })
    
async def find_features(companyId)->List[Feature]:
    company =await get_company(company_id=companyId)
    return await db.feature.find_many(where={"companyId":company.id})
