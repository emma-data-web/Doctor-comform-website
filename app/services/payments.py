import stripe
from app.db.payments import create_payment_record
from sqlalchemy.orm import Session
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(db: Session, email: str, quantity: int, type_: str, item_id: str):
    
    session = stripe.checkout.Session.create(
        payment_method_types=["card"], 
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"{type_.capitalize()} Purchase",
                    "metadata": {
                        "type": type_,
                        "item_id": item_id
                    }
                },
                "unit_amount": 5000  # $50,
            },
            "quantity": quantity
        }],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL
    )

    # 2 Save payment record in DB
    create_payment_record(db, email, session.id, type_, item_id, quantity)

    return session.url