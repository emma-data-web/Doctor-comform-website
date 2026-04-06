from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.payments import BuyRequest
from app.services.payments import create_checkout_session
from app.dependencies import get_db   
from fastapi.responses import HTMLResponse


router = APIRouter()

@router.post("/buy-ticket")
def buy_ticket(request: BuyRequest, db: Session = Depends(get_db)):
    
    checkout_url = create_checkout_session(
        db=db,
        email=request.email,
        quantity=request.quantity,
        type_="ticket",  
        item_id=request.item_id
    )
    return {"checkout_url": checkout_url}






@router.get("/welcome/{ticket_id}", response_class=HTMLResponse)
def welcome(ticket_id: str):
    return """
    <html>
        <body style="display:flex; justify-content:center; align-items:center; height:100vh; background:#000; color:#fff; font-family:Arial; text-align:center;">
            <div>
                <h1> Welcome to Brunch & Pray!</h1>
                <p>Your ticket has been confirmed.</p>
                <p>Enjoy the experience! </p>
            </div>
        </body>
    </html>
    """
