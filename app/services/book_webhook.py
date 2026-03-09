import stripe
from app.core.config import settings
from app.models.payments import BookPayment
from app.services.book_email import send_physical_book_email


async def handle_book_payment(payload, sig_header, db):

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return {"status": "invalid signature"}

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]
        metadata = session.get("metadata", {})

        if metadata.get("product_type") == "book":

            book_payment = BookPayment(
                stripe_session_id=session.get("id"),
                book_title=metadata.get("book_title", ""),
                quantity=int(metadata.get("quantity", 1)),
                status="paid",
                buyer_email=metadata.get("buyer_email", ""),
                buyer_name=metadata.get("buyer_name", ""),
                buyer_address=metadata.get("buyer_address", ""),
                buyer_phone=metadata.get("buyer_phone")  
            )

            db.add(book_payment)
            db.commit()

            await send_physical_book_email(
                buyer_name=book_payment.buyer_name,
                buyer_email=book_payment.buyer_email,
                buyer_address=book_payment.buyer_address,
                book_title=book_payment.book_title,
                quantity=book_payment.quantity
            )

    return {"status": "ok"}