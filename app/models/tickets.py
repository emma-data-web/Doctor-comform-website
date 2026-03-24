from sqlalchemy import Column, String, Boolean, DateTime
from app.models.payments import Base
from datetime import datetime
import uuid



class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_email = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)  
    qr_code = Column(String, nullable=True)      
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)