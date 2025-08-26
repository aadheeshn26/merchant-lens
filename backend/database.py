from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SaleDB(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    product = Column(String)
    amount = Column(Float)

class ReviewDB(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    product = Column(String)
    text = Column(Text)
    rating = Column(Integer, nullable=True)

engine = create_engine("sqlite:///merchantlens.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()