# MerchantLens

AI-Powered Business Insights & Assistant for Small Online Sellers

## Project Overview

MerchantLens is an AI-powered assistant designed to empower small online sellers (e.g., on Etsy, Gumroad, or Instagram shops) by analyzing sales data, customer reviews, and traffic to provide actionable insights. It offers sales trend analysis, sentiment analysis on reviews, and will include machine learning-driven recommendations for pricing, product bundling, and SEO-optimized product listings. Built with a modular architecture inspired by Shopify’s admin ecosystem, it features a FastAPI backend, Remix.js frontend (in progress), and AI integrations. The goal is a modular, Shopify-aligned MVP, as I'm currently recruiting for a Winter 2026 Engineering Internship there

## Features

- Upload sales CSV and parse into structured data
- Analyze total sales, sales by product, and sales trends by week
- Upload customer reviews and compute sentiment (positive/negative/neutral)
- Modular API design for extensibility (future: pricing recommendations, NLP assistant)

## Tech Stack

- **Backend**: Python, FastAPI, pandas, TextBlob (sentiment analysis)
- **Frontend**: React, Tailwind CSS (planned for Week 2)
- **ML/AI**: TextBlob for sentiment analysis, scikit-learn/Surprise (planned for recommendations), OpenAI API (planned for NLP)
- **Data**: CSV files (sales, reviews), SQLite (planned for Week 2)
- **Tools**: Git, VS Code, Vercel/Heroku (planned for deployment)

## Setup Instructions

1. Clone repo: `git clone https://github.com/aadheeshn26/MerchantLens.git`
2. Navigate to backend: `cd backend`
3. Create virtual env: `python -m venv venv`
4. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run server: `uvicorn main:app --reload`
7. Test APIs at `http://127.0.0.1:8000/docs` (swagger docs)

## Demo

(TBD: Screenshots and demo video will be added after frontend completion in Week 2-3)

## Development Progress

- **Week 1, Day 1**: Initialized GitHub repo, set up FastAPI backend with basic endpoints.
- **Week 1, Day 2**: Added CSV upload for sales data, `Sale` model, and basic analysis (total sales, by product).
- **Week 1, Day 3**: Implemented weekly sales trends and sentiment analysis with `Review` model.
