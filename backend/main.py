from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from models import Sale, Review
from typing import List
from analysis import (
    compute_total_sales,
    compute_sales_by_product,
    compute_sales_by_week,
    compute_review_sentiment,
    add_sale,
    add_review,
)
from recommendations import get_recommendations
from fastapi.middleware.cors import CORSMiddleware
import io
from nlp import process_query

app = FastAPI(title="MerchantLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to MerchantLens API"}


# Upload CSV endpoint
@app.post("/upload-sales")
async def upload_sales(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        # Read CSV into pandas DataFrame
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        # Validate and convert to Sale objects
        for _, row in df.iterrows():
            sale = Sale(
                date=pd.to_datetime(row["date"]),
                product=row["product"],
                amount=float(row["amount"]),
            )
            add_sale(sale)
        return {"message": f"Uploaded {len(df)} sales records"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


# Get request total sales
@app.get("/sales/total")
def get_total_sales():
    total = compute_total_sales()
    return {"total_sales": round(total, 2)}


# Get request for total sales for single product
@app.get("/sales/by-product")
def get_sales_by_product():
    return compute_sales_by_product()


# Sales analysis by week
@app.get("/sales/by-week")
def get_sales_by_week():
    return compute_sales_by_week()


# Upload reviews endpoint
@app.post("/upload-reviews")
async def upload_reviews(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        for _, row in df.iterrows():
            review = Review(
                date=pd.to_datetime(row["date"]),
                product=row["product"],
                text=row["text"],
                rating=int(row["rating"]) if pd.notna(row["rating"]) else None,
            )
            add_review(review)
        return {"message": f"Uploaded {len(df)} review records"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")


@app.get("/reviews/sentiment")
def get_review_sentiment():
    return compute_review_sentiment()


@app.get("/recommendations/pricing")
def get_pricing_recommendations():
    return get_recommendations()


@app.post("/nlp/query")
async def process_nlp_query(query: str):
    return process_query(query)
