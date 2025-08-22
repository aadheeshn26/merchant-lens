import pandas as pd
from typing import List, Dict
from models import Sale, Review
from textblob import TextBlob
from datetime import datetime

# In-memory storage for sales & reviews (SQLite later)
sales_data: List[Sale] = []
reviews_data: List[Review] = []


def add_sale(sale: Sale):
    sales_data.append(sale)


def add_review(review: Review):
    reviews_data.append(review)


# Analysis functions
def compute_total_sales() -> float:
    return sum(sale.amount for sale in sales_data)


def compute_sales_by_product() -> Dict[str, float]:
    result = {}
    for sale in sales_data:
        result[sale.product] = result.get(sale.product, 0) + sale.amount
    return result


def compute_sales_by_week() -> Dict[str, float]:
    df = pd.DataFrame([sale.model_dump() for sale in sales_data])
    if df.empty:
        return {}
    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week
    df["year"] = df["date"].dt.year
    weekly_sales = df.groupby(["year", "week"])["amount"].sum().to_dict()
    return {
        f"{year}-W{week:02d}": round(amount, 2)
        for (year, week), amount in weekly_sales.items()
    }


def compute_review_sentiment() -> Dict[str, Dict[str, any]]:
    result = {}
    for review in reviews_data:
        blob = TextBlob(review.text)
        sentiment = blob.sentiment.polarity
        result[review.text] = {
            "product": review.product,
            "sentiment": (
                "positive"
                if sentiment > 0
                else "negative" if sentiment < 0 else "neutral"
            ),
            "polarity": round(sentiment, 2),
        }
    return result
