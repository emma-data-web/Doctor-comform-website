from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import stripe
from app.core.config import settings
from app.db.payments import mark_payment_paid
from app.services.tickets import create_ticket_with_qr
from app.services.email import send_ticket_email
from app.models.payments import BookPayment
from app.services.book_email import send_physical_book_email
from app.dependencies import get_db  

router = APIRouter()

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return {"status": "invalid signature"}
    except Exception:
        return {"status": "error processing webhook"}

    
    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        metadata = session_data.get("metadata", {})

        product_type = metadata.get("type") or metadata.get("product_type")

        if product_type == "ticket":
            stripe_session_id = session_data.get("id")
            payment = mark_payment_paid(db, stripe_session_id)

            if payment:
                for _ in range(payment.quantity):
                    ticket = create_ticket_with_qr(db, payment.buyer_email, payment.id)
                    await send_ticket_email(ticket.buyer_email, ticket.qr_code)

        elif product_type == "book":
            book_payment = BookPayment(
                stripe_session_id=session_data.get("id"),
                book_title=metadata.get("book_title", ""),
                quantity=int(metadata.get("quantity", 1)),
                status="paid",
                buyer_email=metadata.get("buyer_email", ""),
                buyer_name=metadata.get("buyer_name", ""),
                buyer_address=metadata.get("buyer_address", ""),
                buyer_phone=metadata.get("buyer_phone", "")
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

        else:
            return {"status": "ignored product type"}

        return {"status": "success"}

    return {"status": "ignored event"}