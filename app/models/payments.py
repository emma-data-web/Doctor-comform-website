from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_email = Column(String, nullable=False)
    stripe_session = Column(String, nullable=False)
    type = Column(String, nullable=False)   #  either of ticket or book 
    item_id = Column(String, nullable=False)    # ID of event or book
    quantity = Column(Integer, default=1)
    paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)



class BookPayment(Base):
    __tablename__ = "book_payments"

    id = Column(Integer, primary_key=True, index=True)
    stripe_session_id = Column(String, unique=True, index=True)
    book_title = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    status = Column(String, default="pending")  

    buyer_email = Column(String, nullable=False)
    buyer_name = Column(String, nullable=False)
    buyer_address = Column(String, nullable=False)
    buyer_phone = Column(String, nullable=True) 