# MerchantLens Planning Document

## Project Overview

MerchantLens is an AI-powered assistant for small online sellers (Etsy, Gumroad, Instagram shops) to analyze sales, reviews, and traffic, delivering insights via a natural language interface. It provides sales analytics, sentiment analysis, pricing/bundling recommendations, and SEO-optimized product listings. The goal is a modular, Shopify-aligned MVP for my internship application’s behavioral interview.

## Core Features (MVP)

1. **Data Upload**:
   - Handle CSV uploads for sales (date, product, amount) and reviews (date, product, text, rating).
   - Current: Sales and review CSV upload implemented (Day 2-3).
2. **Basic Analysis**:
   - Compute total sales, sales by product, and weekly trends.
   - Current: Implemented total sales, by-product, and by-week analysis (Day 2-3).
3. **ML Insights**:
   - Sentiment analysis on reviews (positive/negative/neutral).
   - Pricing recommendations (e.g., based on demand trends).
   - Product bundling suggestions (e.g., pair high-performing products).
   - Current: Sentiment analysis with TextBlob implemented (Day 3). Pricing/bundling planned for Week 2.
4. **NLP Assistant**:
   - Answer queries like “Compare sales last week vs. previous” with text and chart data.
   - Current: Planned for Week 2 with OpenAI API.
5. **SEO Suggestions**:
   - Generate keyword-rich product titles/descriptions using NLP.
   - Current: Planned for Week 2-3.
6. **Modularity**:
   - Plugin-like architecture for adding new insights (e.g., pricing, SEO plugins).
   - Current: Planned for Week 2 with base plugin structure.

## ML Plan

- **Sentiment Analysis**: TextBlob for review sentiment (positive/negative/neutral). Input: CSV with review text, rating. Status: Implemented (Day 3).
- **Recommendations**: scikit-learn/Surprise for pricing (regression) and bundling (matrix factorization). Input: Sales data. Status: Planned for Week 2.
- **NLP Assistant**: OpenAI API for query parsing and response generation. Input: User text, output: Text + chart data. Status: Planned for Week 2.
- **Timeline**:
  - Week 1: Sentiment analysis, basic data processing.
  - Week 2: Pricing/bundling recommendations, NLP assistant, frontend setup.
  - Week 3: SEO suggestions, frontend polish, deployment.

## Edge Cases

- **Empty CSV**: Handle with error messages (implemented in upload endpoints).
- **Invalid Data**: Validate via Pydantic models (e.g., positive amounts, valid ratings).
- **Future**: Handle missing columns, large files, or API rate limits (e.g., OpenAI).

## Tech Stack

- Backend: Python, FastAPI, pandas, TextBlob
- Frontend: React, Tailwind CSS
- ML/AI: TextBlob, scikit-learn/Surprise, OpenAI API
- Data: CSV, SQLite (planned)
- Tools: Git, VS Code, Vercel/Heroku
