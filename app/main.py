from fastapi import FastAPI

from app.routes import payments, webhook, book_order 

app = FastAPI(title="Tickets & Books Payment System")


app.include_router(payments.router, prefix="/tickets")  # handles /tickets/buy
app.include_router(book_order.router, prefix="/books")      # handles /books/buy-book
app.include_router(webhook.router, prefix="/webhook") # handles /webhook/stripe-webhook