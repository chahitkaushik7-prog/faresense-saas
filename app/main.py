from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal, engine
from app.models import Base, Ride, Booking
from app.pricing_engine import calculate_price

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# -----------------------------
# Create Tables on Startup
# -----------------------------


# -----------------------------
# DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Root Check
# -----------------------------
@app.get("/")
def root():
    return {"message": "Bus Ticket Pricing SaaS Running 🚀"}


# -----------------------------
# Test DB
# -----------------------------
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"status": "connected"}


# -----------------------------
# Create Ride API
# -----------------------------
@app.post("/rides")
def create_ride(
    route_name: str,
    base_price: float,
    total_seats: int,
    db: Session = Depends(get_db),
):

    ride = Ride(
        route_name=route_name,
        base_price=base_price,
        total_seats=total_seats,
        current_price=base_price,
    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return {
        "message": "Ride created successfully",
        "ride_id": ride.id,
        "current_price": ride.current_price,
    }


# -----------------------------
# Book Seat API
# -----------------------------
@app.post("/book")
def book_seat(
    ride_id: int,
    seats: int,
    db: Session = Depends(get_db),
):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        return {"error": "Ride not found"}

    # Check seat availability
    total_booked = (
        db.query(func.sum(Booking.seats_booked))
        .filter(Booking.ride_id == ride_id)
        .scalar()
        or 0
    )

    if total_booked + seats > ride.total_seats:
        return {"error": "Not enough seats available"}

    # Create booking
    booking = Booking(
        ride_id=ride_id,
        seats_booked=seats,
    )

    db.add(booking)
    db.commit()

    # -----------------------------
    # OCCUPANCY CALCULATION
    # -----------------------------
    total_booked += seats
    occupancy = total_booked / ride.total_seats

    # -----------------------------
    # PRICE UPDATE
    # -----------------------------
    new_price = calculate_price(ride.base_price, occupancy)
    ride.current_price = new_price
    db.commit()

    return {
        "message": "Seat booked successfully",
        "occupancy": round(occupancy, 2),
        "updated_price": ride.current_price,
    }


# -----------------------------
# Get Ride Details
# -----------------------------
@app.get("/rides/{ride_id}")
def get_ride(ride_id: int, db: Session = Depends(get_db)):

    ride = db.query(Ride).filter(Ride.id == ride_id).first()

    if not ride:
        return {"error": "Ride not found"}

    total_booked = (
        db.query(func.sum(Booking.seats_booked))
        .filter(Booking.ride_id == ride_id)
        .scalar()
        or 0
    )

    occupancy = total_booked / ride.total_seats

    return {
        "ride_id": ride.id,
        "route": ride.route_name,
        "base_price": ride.base_price,
        "current_price": ride.current_price,
        "total_seats": ride.total_seats,
        "booked_seats": total_booked,
        "occupancy": round(occupancy, 2),
    }