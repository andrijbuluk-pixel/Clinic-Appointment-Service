import stripe
from django.conf import settings


def create_stripe_session(request, money_to_pay, service_name):
    stripe.api_key = settings.STRIPE_API_KEY

    if request:
        base_host = request.build_absolute_uri("/").rstrip("/")
    else:
        base_host = getattr(settings, "BASE_URL", "http://127.0.0.1:8000").rstrip("/")

    success_url = f"{base_host}/api/payment/success/?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{base_host}/api/payment/cancel/"

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(money_to_pay * 100),
                    "product_data": {
                        "name": service_name
                    }
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url
    )

    return session
