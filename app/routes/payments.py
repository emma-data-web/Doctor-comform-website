from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.payments import BuyRequest
from app.services.payments import create_checkout_session
from app.dependencies import get_db   

router = APIRouter()

@router.post("/buy-ticket")
def buy_ticket(request: BuyRequest, db: Session = Depends(get_db)):
    """
    Create a Stripe checkout session for tickets.
    """
    checkout_url = create_checkout_session(
        db=db,
        email=request.email,
        quantity=request.quantity,
        type_="ticket",  
        item_id=request.item_id
    )
    return {"checkout_url": checkout_url}