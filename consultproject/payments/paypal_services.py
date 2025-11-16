import requests
from django.conf import settings


PAYPAL_BASE = "https://api-m.sandbox.paypal.com"  # Production → api-m.paypal.com


def get_access_token():
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    data = {"grant_type": "client_credentials"}

    response = requests.post(
        f"{PAYPAL_BASE}/v1/oauth2/token",
        data=data,
        auth=auth,
    )
    return response.json()["access_token"]


def create_paypal_order(amount):
    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    body = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": str(amount)}
        }]
    }

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders",
        json=body,
        headers=headers
    )

    return response.json()


def capture_paypal_order(order_id):
    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{PAYPAL_BASE}/v2/checkout/orders/{order_id}/capture",
        headers=headers
    )

    return response.json()
