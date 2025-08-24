# MerchantLens Planning Document

## Project Overview

MerchantLens is an AI-powered assistant for small online sellers (Etsy, Gumroad, Instagram shops) to analyze sales, reviews, and traffic, delivering insights via a natural language interface. It provides sales analytics, sentiment analysis, deep learning-based recommendations, and SEO-optimized product listings. The goal is a modular, Shopify-aligned MVP for my internship application’s behavioral interview (lifestory).

## Core Features (MVP)

1. **Data Upload**:
   - Handle CSV uploads for sales (date, product, amount) and reviews (date, product, text, rating).
   - Current: Implemented for sales and reviews (Day 2-3).
2. **Basic Analysis**:
   - Compute total sales, sales by product, and weekly trends.
   - Current: Implemented (Day 2-3).
3. **ML Insights**:
   - Sentiment analysis on reviews (positive/negative/neutral).
   - Pricing recommendations and product bundling using TensorFlow Recommenders.
   - Current: Sentiment (TextBlob, Day 3), recommendations (TFRS, Day 4).
4. **NLP Assistant**:
   - Answer queries like “Compare sales last week vs. previous” with text and chart data.
   - Current: Planned for Week 1, Day 5 with OpenAI API.
5. **SEO Suggestions**:
   - Generate keyword-rich product titles/descriptions using NLP.
   - Current: Planned for Week 2-3.
6. **Modularity**:
   - Plugin-like architecture for adding new insights (e.g., pricing, SEO plugins).
   - Current: Analysis module implemented (Day 4), plugin system planned for Week 2.

## ML Plan

- **Sentiment Analysis**: TextBlob for review sentiment. Input: CSV with review text, rating. Status: Implemented (Day 3).
- **Recommendations**: TensorFlow Recommenders for pricing (discount suggestions) and bundling (product retrieval). Input: Sales data. Status: Implemented basic retrieval model (Day 4).
- **NLP Assistant**: OpenAI API for query parsing and response generation. Input: User text, output: Text + chart data. Status: Planned for Day 5.
- **Timeline**:
  - Week 1: Sentiment, recommendations, frontend setup.
  - Week 2: NLP assistant, enhanced recommendations, frontend polish, SQLite integration.
  - Week 3: SEO suggestions, deployment, demo.

## Edge Cases

- Empty CSV: Handled with error messages (upload endpoints).
- Invalid Data: Validated via Pydantic models (e.g., positive amounts, valid ratings).
- Future: Handle missing columns, large datasets, TFRS scalability, API rate limits.

## Tech Stack

- Backend: Python 3.12.5, FastAPI, pandas, TextBlob, TensorFlow Recommenders (tensorflow-metal for local dev)
- Frontend: Remix.js, Tailwind CSS
- ML/AI: TextBlob, TensorFlow Recommenders, OpenAI API
- Data: CSV, SQLite (planned)
- Tools: Git, VS Code, pyenv, Vercel/Heroku
