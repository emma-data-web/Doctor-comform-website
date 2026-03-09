from sqlalchemy.orm import Session
from app.models.tickets import Ticket

def create_ticket(db: Session, buyer_email: str, payment_id: str, qr_code: str):
    ticket = Ticket(
        buyer_email=buyer_email,
        payment_id=payment_id,
        qr_code=qr_code
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket