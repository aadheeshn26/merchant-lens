from fastapi import FastAPI

app = FastAPI(
    title="MerchantLens API", description="AI-Powered Insights for Small Sellers"
)


# Basic OOP Class Example: Merchant (encapsulates data)
class Merchant:
    def __init__(self, name: str):
        self._name = name  # Private attribute (encapsulation)
        self._sales = []  # Will hold sales data later

    def add_sale(self, amount: float):
        if amount < 0:
            raise ValueError("Sale amount cannot be negative")
        self._sales.append(amount)

    def get_total_sales(self) -> float:
        return sum(self._sales)  # Abstraction: User gets total without seeing list

    def get_name(self) -> str:
        return self._name


# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to MerchantLens API"}


# Example Endpoint: Create a merchant and add mock sale
@app.get("/merchant/{name}")
def get_merchant(name: str):
    merchant = Merchant(name)
    merchant.add_sale(100.50)  # Mock sale
    merchant.add_sale(200.75)
    return {
        "merchant_name": merchant.get_name(),
        "total_sales": merchant.get_total_sales(),
    }
