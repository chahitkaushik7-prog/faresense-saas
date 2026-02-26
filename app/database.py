import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine("postgresql://postgres:GGcljqMuIGDUsUFUyFOhldaefplunoTh@postgres.railway.internal:5432/railway")
SessionLocal = sessionmaker(bind=engine)
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)