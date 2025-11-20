from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import stripe
from pyseoanalyzer.analyzer import analyze_url

import os

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# Environment: Render → add these in Dashboard
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
public_key = os.getenv("STRIPE_PUBLIC_KEY")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "stripe_public": public_key})

@app.post("/create-checkout-session")
def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "SEO Website Analyse"},
                "unit_amount": 2000,  # €20
            },
            "quantity": 1
        }],
        mode="payment",
        success_url="https://YOUR-RENDER-APP.onrender.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://YOUR-RENDER-APP.onrender.com/cancel",
    )
    return {"id": session.id}

@app.get("/success")
def success(request: Request, session_id: str):
    # Haal de betaal info op:
    session = stripe.checkout.Session.retrieve(session_id)
    url = session.get("metadata", {}).get("url", None)

    return templates.TemplateResponse("success.html", {"request": request})

@app.post("/analyze")
def analyze(url: str = Form(...)):
    result = analyze_url(url)
    return JSONResponse(result)
