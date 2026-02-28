from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    total_seats = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="ride")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"))
    seats_booked = Column(Integer, nullable=False)
    booking_time = Column(DateTime, default=datetime.utcnow)

    ride = relationship("Ride", back_populates="bookings")

    class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    route_name = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    total_seats = Column(Integer, nullable=False)
    current_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="ride")