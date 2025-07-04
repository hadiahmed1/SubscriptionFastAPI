from pydantic import BaseModel

class OrderCreate(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str 
    razorpay_signature: str
