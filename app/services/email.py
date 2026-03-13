from fastapi_mail import FastMail, MessageSchema, MessageType
import base64
from app.core.email import conf

async def send_ticket_email(to_email: str, qr_base64: str):
    # Convert base64 QR to bytes
    qr_bytes = base64.b64decode(qr_base64)
    
    message = MessageSchema(
        subject="Your Ticket Is Ready!",
        recipients=[to_email],
        body="""
        <p>Here is your ticket. Scan the QR code at the event.</p>
        """,
        subtype=MessageType.html
    )
    
    fm = FastMail(conf)
    
    # Send email with QR code 
    await fm.send_message(message, files=[("ticket.png", qr_bytes)])