
import asyncio
from app.core.email import conf  
from fastapi_mail import FastMail, MessageSchema
from app.core.config import settings

async def test_ticket_email():
    message = MessageSchema(
        subject="Test ",
        recipients=[settings.MAIL_FROM],  
        body="working.",
        subtype="plain"
    )

    
    print(settings.MAIL_USERNAME)
    print(settings.MAIL_SERVER)

    fm = FastMail(conf)
    await fm.send_message(message)
    print(" worked")

if __name__ == "__main__":
    asyncio.run(test_ticket_email())