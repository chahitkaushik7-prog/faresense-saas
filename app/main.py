from fastapi import FastAPI
import os
from sqlalchemy import create_engine, text

from app.models import Base
from app.pricing_engine import calculate_price

app = FastAPI()

# Create tables
# Base.metadata.create_all(bind=engine)


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


@app.get("/test-db")
def test_db():
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")

        if not DATABASE_URL:
            return {"error": "DATABASE_URL not set"}

        engine = create_engine(DATABASE_URL)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {"status": "connected"}

    except Exception as e:
        return {"error": str(e)}