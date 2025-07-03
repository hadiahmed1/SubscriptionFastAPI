from typing import List
from pydantic import BaseModel, Field

class PlanCreate(BaseModel):
    name: str
    description: str
    cost: float = Field(..., ge=0, description="Cost must be non-negative")
    discount: int = Field(0, ge=0, le=100, description="Discount must be between 0 and 100")
    validity: int= Field(30, ge=1, description="Validity must be greater than 0")
    feature_ids: List[str]=[]
