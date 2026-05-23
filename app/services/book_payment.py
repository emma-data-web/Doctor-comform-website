from app.core.config import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_book_payment_session(book_title, quantity, buyer_name, buyer_email, buyer_address, buyer_phone,price: int):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": book_title},
                "unit_amount": int(price * 100),  
            },
            "quantity": quantity
        }],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
        metadata={
            "product_type": "book",
            "book_title": book_title,
            "quantity": quantity,
            "buyer_name": buyer_name,
            "buyer_email": buyer_email,
            "buyer_address": buyer_address,
            "buyer_phone": buyer_phone
        }
    )
    return session.url