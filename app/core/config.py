import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
GMAIL_ID = "hadiahmed0112@gmail.com"
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

RAZORPAY_KEY_SECRET=os.getenv("RAZORPAY_KEY_SECRET")
RAZORPAY_KEY_ID=os.getenv("RAZORPAY_KEY_ID")