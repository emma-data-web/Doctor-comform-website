import stripe
from app.services.email import send_ticket_email
from app.db.payments import mark_payment_paid
from app.services.tickets import create_ticket_with_qr
from app.core.config import settings


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

async def handle_stripe_event(payload: bytes, sig_header: str, db):

    
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return {"status": "invalid signature"}
    except Exception:
        return {"status": "error processing webhook"}

    
    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        stripe_session_id = session_data["id"]

        
        payment = mark_payment_paid(db, stripe_session_id)

        #  Generate QR tickets 
        if payment and payment.type == "ticket":
            for _ in range(payment.quantity):
                ticket = create_ticket_with_qr(db, payment.buyer_email, payment.id)
                await send_ticket_email(ticket.buyer_email, ticket.qr_code)
                

        return {"status": "success"}

    
    return {"status": "ignored event"}