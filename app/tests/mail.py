import asyncio
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.core.email import conf  

async def test_mailtrap():
    message = MessageSchema(
        subject="Mailtrap Test Email",
        recipients=["anyemail@example.com"],  
        body="<p>its working fine!</p>",
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    print("Test email sent! Check Mailtrap inbox.")


if __name__ == "__main__":
    asyncio.run(test_mailtrap())