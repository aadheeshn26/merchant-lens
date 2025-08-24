from openai import OpenAI
from typing import Dict, Any
from analysis import (
    sales_data,
    reviews_data,
    compute_total_sales,
    compute_sales_by_week,
    compute_review_sentiment,
)
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def process_query(query: str) -> Dict[str, Any]:
    # Fetch analysis data
    total_sales = compute_total_sales()
    weekly_sales = compute_sales_by_week()
    sentiment = compute_review_sentiment()

    # Prepare context for OpenAI
    context = f"""
    You are MerchantLens, an AI assistant for small online sellers.
    Sales data: Total sales = ${total_sales:.2f}.
    Weekly sales: {weekly_sales}.
    Review sentiment: {sentiment}.
    Answer the user's query concisely, using the data above. If the query asks for a comparison or analysis not directly available, provide a reasonable response based on the data. Keep it professional and actionable.
    Query: {query}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": query},
            ],
            max_tokens=150,
        )
        answer = response.choices[0].message.content
        return {"query": query, "answer": answer}
    except Exception as e:
        return {"query": query, "answer": f"Error processing query: {str(e)}"}
