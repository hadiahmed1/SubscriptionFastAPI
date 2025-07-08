from fastapi import APIRouter, Depends, HTTPException, status
import razorpay
from app.core.dependancy import get_current_user
from app.schemas.order_schema import OrderCreate
from app.services.plan_service import find_plan_byID
from prisma.models import Plan, User
from app.db.client import db
from app.services.suscription_service import suscribe
from app.core.razorpay import razorpay_client


router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/verify")
async def verify_signature(data: OrderCreate):
    try:
        # Verify signature
        razorpay_client.utility.verify_payment_signature(
            {
                "razorpay_order_id": data.razorpay_order_id,
                "razorpay_payment_id": data.razorpay_payment_id,
                "razorpay_signature": data.razorpay_signature,
            }
        )
        # create subscription
        order = await db.order.find_first(where={"order_id": data.razorpay_order_id})
        subscription = await suscribe(planId=order.planId, userId=order.userId)
        return subscription
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Signature verification failed")


@router.post("/{plan_id}", status_code=status.HTTP_201_CREATED)
async def create_order(plan_id, user: User = Depends(get_current_user)):
    plan: Plan = await find_plan_byID(plan_id)
    amount = plan.cost * (100 - plan.discount)
    currency = "INR"
    order_data = {"amount": amount, "currency": currency}
    razorpay_order = razorpay_client.order.create(data=order_data)
    # making order
    await db.order.create(
        data={"order_id": razorpay_order["id"], "userId": user.id, "planId": plan.id}
    )
    return {"order_id": razorpay_order["id"], "amount": amount}
