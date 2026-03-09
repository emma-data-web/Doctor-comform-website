from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_email = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)  # link to Payment
    qr_code = Column(String, nullable=True)      # path or base64 of QR
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)