
from pydantic import BaseModel



class BookPurchaseRequest(BaseModel):
    book_title: str
    quantity: int
    buyer_name: str
    buyer_email: str
    buyer_address: str
    buyer_phone: str = None
    price: float