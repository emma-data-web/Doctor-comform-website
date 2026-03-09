from sqlalchemy.orm import Session
from app.models.payments import Payment

def create_payment_record(db: Session, buyer_email: str, stripe_session: str, type_: str, item_id: str, quantity: int):
    payment = Payment(
        buyer_email=buyer_email,
        stripe_session=stripe_session,
        type=type_,
        item_id=item_id,
        quantity=quantity,
        paid=False
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def mark_payment_paid(db: Session, stripe_session: str):
    payment = db.query(Payment).filter(Payment.stripe_session == stripe_session).first()
    if payment:
        payment.paid = True
        db.commit()
    return payment