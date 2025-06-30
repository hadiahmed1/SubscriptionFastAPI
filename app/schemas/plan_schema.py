from pydantic import BaseModel, Field

class PlanCreate(BaseModel):
    name: str
    description: str
    cost: float = Field(..., ge=0, description="Cost must be non-negative")
    discount: int = Field(..., ge=0, le=100, description="Discount must be between 0 and 100")
