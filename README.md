# MerchantLens

AI-Powered Business Insights & Assistant for Small Online Sellers - think Shopify Sidekick, but generalized for small online sellers.

## Project Overview

MerchantLens is an AI-powered assistant designed to empower small online sellers (e.g., on Etsy, Gumroad, or Instagram shops) by analyzing sales data, customer reviews, and traffic to provide actionable insights. It offers sales trend analysis, sentiment analysis on reviews, deep learning-based product recommendations, and a web interface. I'm building this with a modular architecture inspired by Shopify’s admin ecosystem, featuring a FastAPI backend and Remix.js frontend (aligned with Shopify’s Hydrogen). The goal is a modular, Shopify-aligned MVP, as I'm currently recruiting for a Winter 2026 Engineering Internship there :)

## Features

- Upload sales CSV and parse into structured data
- Analyze total sales, sales by product, and sales trends by week
- Upload customer reviews and compute sentiment (positive/negative/neutral)
- Deep learning-based product recommendations and pricing suggestions using TensorFlow Recommenders
- Frontend dashboard with Remix.js to display insights
- Modular API design for extensibility (future: NLP assistant, SEO suggestions)

## Tech Stack

- **Backend**: Python 3.12.5, FastAPI, pandas, TextBlob (sentiment), TensorFlow Recommenders (recommendations)
- **Frontend**: Remix.js, Tailwind CSS
- **ML/AI**: TextBlob, TensorFlow Recommenders with tensorflow-metal (local dev), OpenAI API (planned)
- **Data**: CSV files (sales, reviews), SQLite
- **Tools**: Git, VS Code, pyenv, Vercel/Heroku (planned for deployment)

## Setup Instructions

1. Clone repo: `git clone https://github.com/aadheeshn26/MerchantLens.git`
2. **Backend**:
   - Navigate: `cd backend`
   - Set Python 3.12.5: `pyenv local 3.12.5`
   - Create virtual env: `python -m venv venv312`
   - Activate: `source venv312/bin/activate` (Mac/Linux) or `venv312\Scripts\activate` (Windows)
   - Install: `pip install -r requirements.txt`
   - Run: `uvicorn main:app --reload`
   - Test APIs: `http://127.0.0.1:8000/docs`
3. **Frontend**:
   - Navigate: `cd frontend/merchantlens-frontend`
   - Install: `npm install`
   - Run: `npm run dev`
   - View: `http://localhost:5173`

## Demo

(TBD: Screenshots and demo video will be added after frontend completion in Week 2-3)
