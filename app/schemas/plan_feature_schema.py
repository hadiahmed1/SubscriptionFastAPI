from pydantic import BaseModel

class PlanFeatureCreate(BaseModel):
    planId:str
    featureId:str
