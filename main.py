from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import stripe

# Import de bestaande analyzer
from pyseoanalyzer.analyzer import analyze

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Zet deze in Render Environment Variables
stripe.api_key = "STRIPE_SECRET_KEY"

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
def run_analysis(url: str = Form(...)):
    # pyseoanalyzer analyseert de URL en geeft een dict terug
    result = analyze_url(url)  
    return JSONResponse(result)

@app.post("/create-checkout-session")
def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': 'SEO Analyse'},
                'unit_amount': 2000,  # €20
            },
            'quantity': 1
        }],
        mode='payment',
        success_url='https://jouw-app.onrender.com/success',
        cancel_url='https://jouw-app.onrender.com/cancel',
    )
    return {"id": session.id}

