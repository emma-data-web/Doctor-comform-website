from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import stripe
from app.core.config import settings
from app.db.payments import mark_payment_paid
from app.services.tickets import create_ticket_with_qr
from app.services.email import send_ticket_email
from app.models.payments import BookPayment, Payment
from app.services.book_email import send_physical_book_email
from app.dependencies import get_db  
from app.services.book_email import send_physical_book_owner_email

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

            
            payment = db.query(Payment).filter(Payment.stripe_session == stripe_session_id).first()

            if not payment:
                return {"status": "payment not found"}

            if payment.paid == True:
                print("Duplicate ticket webhook")
                return {"status": "already processed"}

            
            mark_payment_paid(db, stripe_session_id)

            for _ in range(payment.quantity):
                ticket = create_ticket_with_qr(db, payment.buyer_email, payment.id)
                try: 
                    await send_ticket_email(ticket.buyer_email, ticket.qr_code)
                    print(f"Email sent to {ticket.buyer_email}")
                except Exception as e:
                    print("EMAIL ERROR:", str(e))

        elif product_type == "book":
            print("BOOK WEBHOOK HIT!")
            stripe_session_id = session_data.get("id")
            print(f"Session ID: {stripe_session_id}")
            print(f"Metadata: {metadata}")
            existing_payment = db.query(BookPayment).filter_by(
                stripe_session_id=stripe_session_id
            ).first()

            if existing_payment:
                print("Duplicate webhook")
                return {"status": "already processed"}

            book_payment = BookPayment(
                stripe_session_id=stripe_session_id,
                book_title=metadata.get("book_title", ""),
                quantity=int(metadata.get("quantity", 1)),
                status="paid",
                buyer_email=metadata.get("buyer_email", ""),
                buyer_name=metadata.get("buyer_name", ""),
                buyer_address=metadata.get("buyer_address", ""),
                buyer_phone=metadata.get("buyer_phone", "")
            )

            try:
                db.add(book_payment)
                db.commit()
            except IntegrityError:
                db.rollback()
                print("Duplicate prevented for database")
                return {"status": "duplicate ignored"}
            
            try:
                await send_physical_book_email(
                    buyer_name=book_payment.buyer_name,
                    buyer_email=book_payment.buyer_email,
                    buyer_address=book_payment.buyer_address,
                    book_title=book_payment.book_title,
                    quantity=book_payment.quantity
                )
                print(f"Book email sent to {book_payment.buyer_email}")

                owner_email = settings.OWNER_EMAIL
                await send_physical_book_owner_email(book_payment, owner_email)
                print(f"Owner email sent to {owner_email}")
            except Exception as e:  
                 print("BOOK EMAIL ERROR:", str(e))

        else:
            return {"status": "ignored product type"}

        return {"status": "success"}

    return {"status": "ignored event"}