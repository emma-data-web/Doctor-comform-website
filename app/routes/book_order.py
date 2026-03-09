from fastapi import APIRouter, Depends
from app.schemas.book_schema import BookPurchaseRequest
from sqlalchemy.orm import Session
from app.models.payments import BookPayment
from app.services.book_payment import create_book_payment_session
from app.dependencies import get_db

router = APIRouter()




@router.post("/buy-book")
def buy_book(request: BookPurchaseRequest, db: Session = Depends(get_db)):
    # Create Stripe session
    session_url = create_book_payment_session(
        book_title=request.book_title,
        quantity=request.quantity,
        buyer_name=request.buyer_name,
        buyer_email=request.buyer_email,
        buyer_address=request.buyer_address,
        buyer_phone=request.buyer_phone
    )

    #  Return session URL to frontend
    return {"checkout_url": session_url}