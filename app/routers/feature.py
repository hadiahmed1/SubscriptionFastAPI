from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependancy import get_current_company
from app.schemas.feature_schema import FeatureCreate
from app.services.feature_service import create_feature, find_features
from prisma.models import User
from prisma.errors import UniqueViolationError

router = APIRouter(prefix="/feature", tags=["Feature"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_feature(
    feature: FeatureCreate, company: User = Depends(get_current_company)
):
    try:
        return await create_feature(company_id=company.id, feature_data=feature)
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Feature with this name already exists for this company.",
        )


@router.get("/{company_id}", status_code=status.HTTP_200_OK)
async def get_features(company_id):
    return await find_features(company_id)
