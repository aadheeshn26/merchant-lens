from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
import pandas as pd
from models import Sale, Review
from analysis import add_sale, add_review, compute_total_sales, compute_sales_by_product, compute_sales_by_week, compute_review_sentiment
from recommendations import get_recommendations
from nlp import process_query
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from sqlalchemy.orm import Session
from seo import generate_seo_content
import io

app = FastAPI(title="MerchantLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to MerchantLens API"}

@app.post("/upload-sales")
async def upload_sales(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        for _, row in df.iterrows():
            sale = Sale(
                date=pd.to_datetime(row['date']),
                product=row['product'],
                amount=float(row['amount'])
            )
            add_sale(sale, db)
        return {"message": f"Uploaded {len(df)} sales records"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@app.post("/upload-reviews")
async def upload_reviews(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        for _, row in df.iterrows():
            review = Review(
                date=pd.to_datetime(row['date']),
                product=row['product'],
                text=row['text'],
                rating=int(row['rating']) if pd.notna(row['rating']) else None
            )
            add_review(review, db)
        return {"message": f"Uploaded {len(df)} review records"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@app.get("/sales/total")
def get_total_sales(db: Session = Depends(get_db)):
    total = compute_total_sales(db)
    return {"total_sales": round(total, 2)}

@app.get("/sales/by-product")
def get_sales_by_product(db: Session = Depends(get_db)):
    return compute_sales_by_product(db)

@app.get("/sales/by-week")
def get_sales_by_week(db: Session = Depends(get_db)):
    return compute_sales_by_week(db)

@app.get("/reviews/sentiment")
def get_review_sentiment(db: Session = Depends(get_db)):
    return compute_review_sentiment(db)

@app.get("/recommendations/pricing")
def get_pricing_recommendations(db: Session = Depends(get_db)):
    return get_recommendations(db)

@app.post("/nlp/query")
async def process_nlp_query(query: str, db: Session = Depends(get_db)):
    return process_query(query, db)

@app.get("/seo/{product}")
def get_seo_content(product: str, db: Session = Depends(get_db)):
    return generate_seo_content(product, db)