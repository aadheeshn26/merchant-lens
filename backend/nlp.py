from openai import OpenAI
from typing import Dict, Any
from analysis import get_sales_data, get_reviews_data, compute_total_sales, compute_sales_by_week, compute_review_sentiment
from database import get_db
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from fastapi import Depends

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_query(query: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    # Fetch analysis data using SQLite
    total_sales = compute_total_sales(db)
    weekly_sales = compute_sales_by_week(db)
    sentiment = compute_review_sentiment(db)
    sales_data = get_sales_data(db)
    reviews_data = get_reviews_data(db)

    # Prepare context for OpenAI
    context = f"""
    You are MerchantLens, an AI assistant for small online sellers.
    Sales data: Total sales = ${total_sales:.2f}.
    Weekly sales: {weekly_sales}.
    Review sentiment: {sentiment}.
    Sales records: {len(sales_data)} entries.
    Review records: {len(reviews_data)} entries.
    Answer the user's query concisely, using the data above. If the query asks for a comparison or analysis not directly available, provide a reasonable response based on the data. Keep it professional and actionable.
    Query: {query}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content
        return {"query": query, "answer": answer}
    except Exception as e:
        return {"query": query, "answer": f"Error processing query: {str(e)}"}