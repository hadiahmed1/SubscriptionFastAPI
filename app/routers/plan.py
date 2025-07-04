from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependancy import get_current_company
from app.schemas.plan_schema import PlanCreate
from app.services.plan_service import create_plan, find_plans
from prisma.models import User
from prisma.errors import UniqueViolationError

router = APIRouter(
    prefix="/plan",
    tags=["Plan"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_plan(plan: PlanCreate,  company: User = Depends(get_current_company)):
    try:
        new_plan = await create_plan(company_id=company.id, plan_data=plan)
        return new_plan
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plan with this name already exists for this company."
        )

@router.get("/",status_code=status.HTTP_200_OK)
async def get_plans():
    return await find_plans()

@router.get("/company",status_code=status.HTTP_200_OK)
async def get_company_plans(company:User=Depends(get_current_company)):
    return await find_plans(where={"companyId":company.id})