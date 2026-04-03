from fastapi import FastAPI

from app.routes import payments, webhook, book_order 

app = FastAPI(title="Brunch and Pray")


app.include_router(payments.router, prefix="/tickets")  
app.include_router(book_order.router, prefix="/books")     
app.include_router(webhook.router)