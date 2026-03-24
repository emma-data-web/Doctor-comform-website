from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.email import conf


async def send_ticket_email(to_email: str, qr_base64: str):
    
    html_content = f"""
    <p>Here is your ticket. Scan the QR code at the event:</p>
    <img src="data:image/png;base64,{qr_base64}" alt="Ticket QR"/>
    """

    message = MessageSchema(
        subject="Your Ticket Is Ready!",
        recipients=[to_email],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)