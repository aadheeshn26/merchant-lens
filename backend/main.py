# backend/main.py
from fastapi import FastAPI

app = FastAPI(title="MerchantLens API")

# Functional approach: Dictionary to store merchant data
merchants = {}  # Key: name, Value: dict with sales list


def add_sale(merchant_name: str, amount: float):
    if amount < 0:
        raise ValueError("Sale amount cannot be negative")
    if merchant_name not in merchants:
        merchants[merchant_name] = {"sales": []}
    merchants[merchant_name]["sales"].append(amount)


def get_total_sales(merchant_name: str) -> float:
    return sum(merchants.get(merchant_name, {"sales": []})["sales"])


@app.get("/")
def read_root():
    return {"message": "Welcome to MerchantLens API"}


@app.get("/merchant/{name}")
def get_merchant(name: str):
    add_sale(name, 100.50)  # Mock sale
    add_sale(name, 200.75)
    return {"merchant_name": name, "total_sales": get_total_sales(name)}
