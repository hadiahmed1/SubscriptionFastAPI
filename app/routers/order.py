from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import RedirectResponse
import razorpay
from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.core.dependancy import get_current_user
from app.services.plan_service import find_plan_byID
from prisma.models import Plan, User


router = APIRouter(prefix="/order", tags=["Order"])

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@router.post("/{plan_id}", status_code=status.HTTP_201_CREATED)
async def create_order(plan_id, user: User = Depends(get_current_user)):
    plan: Plan = await find_plan_byID(plan_id)
    amount = plan.cost*(100-plan.discount)
    currency="INR"
    
    order_data = {
        "amount": amount,
        "currency": currency
    }
    razorpay_order = razorpay_client.order.create(data=order_data)
    return {"order_id": razorpay_order['id'], "amount": amount}



