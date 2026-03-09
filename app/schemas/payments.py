from pydantic import BaseModel

class BuyRequest(BaseModel):
    email: str
    quantity: int
    item_id: str   
    type: str      