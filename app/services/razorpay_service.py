import requests
from requests.auth import HTTPBasicAuth
from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


def create_razor_pay_plan(
    name: str,
    amount: int,
    period: str = "weekly",
    interval: int = 1,
) -> str:

    url = "https://api.razorpay.com/v1/plans"

    data = {
        "period": period,
        "interval": interval,
        "item": {
            "name": name,
            "amount": amount * 100,
            "currency": "INR",
            "description": f"Description for the {name}",
        },
    }

    response = requests.post(
        url,
        json=data,
        auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET),
        headers={"Content-Type": "application/json"},
    )
    print("RAZORPAY ERROR:", response.status_code, response.text)

    response.raise_for_status()
    response.raise_for_status()
    return response.json()["id"]
