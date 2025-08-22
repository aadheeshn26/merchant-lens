from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class Sale(BaseModel):
    date: datetime
    product: str
    amount: float

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

    @field_validator("product")
    @classmethod
    def product_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()

    @field_validator("date")
    @classmethod
    def date_must_be_valid(cls, v):
        if v > datetime.now():
            raise ValueError("Date cannot be in the future")
        return v
