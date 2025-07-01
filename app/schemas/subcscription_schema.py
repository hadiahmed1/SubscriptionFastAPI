from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    planId:str
    userId:str
