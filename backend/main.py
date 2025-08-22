from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from models import Sale
from typing import List
import io
from datetime import datetime

app = FastAPI(title="MerchantLens API")

# In-memory storage for sales (SQLite later)
sales_data: List[Sale] = []


# Analysis functions
def compute_total_sales() -> float:
    return sum(sale.amount for sale in sales_data)


def compute_sales_by_product() -> dict:
    result = {}
    for sale in sales_data:
        result[sale.product] = result.get(sale.product, 0) + sale.amount
    return result


def compute_sales_by_week() -> dict:
    # Convert sales_data to DataFrame for easier grouping
    df = pd.DataFrame([sale.model_dump() for sale in sales_data])
    if df.empty:
        return {}
    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])
    # Group by week (using ISO week number)
    df["week"] = df["date"].dt.isocalendar().week
    df["year"] = df["date"].dt.year
    # Sum amounts by year and week
    weekly_sales = df.groupby(["year", "week"])["amount"].sum().to_dict()
    # Format as "YYYY-WW": amount
    result = {
        f"{year}-W{week:02d}": round(amount, 2)
        for (year, week), amount in weekly_sales.items()
    }
    return result


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
            sales_data.append(sale)
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
