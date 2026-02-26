from fastapi import FastAPI
from app.pricing_engine import calculate_price

app = FastAPI(title="FareSense SaaS API")

@app.get("/")
def root():
    return {"message": "FareSense SaaS Running 🚀"}

@app.get("/calculate")
def calculate(base_price: float, occupancy: float):
    suggested = calculate_price(base_price, occupancy)
    return {
        "base_price": base_price,
        "occupancy": occupancy,
        "suggested_price": suggested
    }