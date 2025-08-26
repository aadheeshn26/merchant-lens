from openai import OpenAI
from analysis import get_sales_data, get_reviews_data
from database import get_db
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from fastapi import Depends
from typing import Dict
from textblob import TextBlob

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_seo_content(product: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    # Fetch related data
    sales = get_sales_data(db)
    reviews = get_reviews_data(db)
    product_sales = [s for s in sales if s.product == product]
    product_reviews = [r for r in reviews if r.product == product]

    # Extract keywords from reviews
    keywords = []
    for review in product_reviews:
        blob = TextBlob(review.text)
        keywords.extend(blob.noun_phrases)

    # Prepare context for OpenAI
    context = f"""
    You are MerchantLens, an AI assistant for small online sellers.
    Product: {product}.
    Sales count: {len(product_sales)}.
    Review keywords: {', '.join(keywords[:3]) if keywords else 'none'}.
    Generate a concise, SEO-optimized product title (under 60 characters) and description (under 150 characters) using the keywords. Ensure the title includes the product name and is keyword-rich.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": "Generate SEO content"}
            ],
            max_tokens=100
        )
        content = response.choices[0].message.content
        # Parse response (assuming format: "Title: ..., Description: ...")
        lines = content.split("\n")
        title = next((line.split(": ")[1] for line in lines if line.startswith("Title")), product)
        description = next((line.split(": ")[1] for line in lines if line.startswith("Description")), f"High-quality {product}.")
        return {"title": title.strip(), "description": description.strip()}
    except Exception as e:
        return {"title": product, "description": f"Error generating SEO: {str(e)}"}