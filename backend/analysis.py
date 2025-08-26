from typing import List, Dict
from models import Sale, Review
from database import get_db, SaleDB, ReviewDB
from sqlalchemy.orm import Session
from sqlalchemy import func
from textblob import TextBlob
import pandas as pd
from datetime import datetime
from fastapi import Depends

def add_sale(sale: Sale, db: Session = Depends(get_db)):
    db_sale = SaleDB(date=sale.date, product=sale.product, amount=sale.amount)
    db.add(db_sale)
    db.commit()

def add_review(review: Review, db: Session = Depends(get_db)):
    db_review = ReviewDB(date=review.date, product=review.product, text=review.text, rating=review.rating)
    db.add(db_review)
    db.commit()

def get_sales_data(db: Session = Depends(get_db)) -> List[SaleDB]:
    return db.query(SaleDB).all()

def get_reviews_data(db: Session = Depends(get_db)) -> List[ReviewDB]:
    return db.query(ReviewDB).all()

def compute_total_sales(db: Session = Depends(get_db)) -> float:
    return db.query(func.sum(SaleDB.amount)).scalar() or 0

def compute_sales_by_product(db: Session = Depends(get_db)) -> Dict[str, float]:
    results = db.query(SaleDB.product, func.sum(SaleDB.amount)).group_by(SaleDB.product).all()
    return {product: amount for product, amount in results}

def compute_sales_by_week(db: Session = Depends(get_db)) -> Dict[str, float]:
    results = db.query(func.strftime('%Y-W%W', SaleDB.date), func.sum(SaleDB.amount)).group_by(func.strftime('%Y-W%W', SaleDB.date)).all()
    return {week: amount for week, amount in results}

def compute_review_sentiment(db: Session = Depends(get_db)) -> Dict[str, Dict[str, any]]:
    reviews = get_reviews_data(db)
    result = {}
    for review in reviews:
        blob = TextBlob(review.text)
        sentiment = blob.sentiment.polarity
        result[review.text] = {
            "product": review.product,
            "sentiment": "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral",
            "polarity": round(sentiment, 2)
        }
    return result