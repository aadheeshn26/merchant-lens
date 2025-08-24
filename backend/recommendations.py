import tensorflow as tf
import numpy as np
from typing import Dict
from collections import Counter
from models import Sale
from analysis import sales_data


def analyze_sales_patterns() -> Dict[str, any]:
    """Analyze sales patterns to generate recommendations using simple statistics"""
    if not sales_data:
        return {"product_popularity": {}, "weekly_trends": {}, "product_cooccurrence": {}}
    
    # Product popularity (total sales count and revenue)
    product_stats = {}
    weekly_sales = {}
    
    for sale in sales_data:
        product = sale.product
        week = sale.date.isocalendar().week
        
        # Product statistics
        if product not in product_stats:
            product_stats[product] = {"count": 0, "revenue": 0.0, "weeks": set()}
        product_stats[product]["count"] += 1
        product_stats[product]["revenue"] += sale.amount
        product_stats[product]["weeks"].add(week)
        
        # Weekly trends
        week_key = f"Week-{week}"
        if week_key not in weekly_sales:
            weekly_sales[week_key] = {}
        if product not in weekly_sales[week_key]:
            weekly_sales[week_key][product] = 0
        weekly_sales[week_key][product] += 1
    
    # Convert sets to counts for JSON serialization
    for product in product_stats:
        product_stats[product]["active_weeks"] = len(product_stats[product]["weeks"])
        del product_stats[product]["weeks"]
    
    # Product co-occurrence (products bought in same week)
    cooccurrence = {}
    for week_data in weekly_sales.values():
        products_in_week = list(week_data.keys())
        for i, product_a in enumerate(products_in_week):
            if product_a not in cooccurrence:
                cooccurrence[product_a] = Counter()
            for j, product_b in enumerate(products_in_week):
                if i != j:  # Don't count self-occurrence
                    cooccurrence[product_a][product_b] += 1
    
    # Convert Counter objects to regular dicts for JSON serialization
    cooccurrence = {k: dict(v) for k, v in cooccurrence.items()}
    
    return {
        "product_popularity": product_stats,
        "weekly_trends": weekly_sales,
        "product_cooccurrence": cooccurrence
    }


def get_recommendations(top_k: int = 3) -> Dict[str, any]:
    """Generate recommendations based on sales patterns and popularity"""
    if not sales_data:
        return {
            "recommendations": [],
            "pricing_suggestions": {},
            "message": "No sales data available for recommendations"
        }
    
    patterns = analyze_sales_patterns()
    product_stats = patterns["product_popularity"]
    cooccurrence = patterns["product_cooccurrence"]
    
    # Get top products by revenue (primary recommendation)
    top_by_revenue = sorted(
        product_stats.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:top_k]
    
    # Get recommendations based on co-occurrence patterns
    cooccurrence_recs = []
    if cooccurrence:
        # Find the most sold product and its co-occurring products
        most_sold_product = max(product_stats.keys(), key=lambda p: product_stats[p]["count"])
        if most_sold_product in cooccurrence:
            cooccurrence_recs = sorted(
                cooccurrence[most_sold_product].items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_k]
    
    # Combine and deduplicate recommendations
    all_recommendations = set()
    
    # Add top revenue products
    for product, stats in top_by_revenue:
        all_recommendations.add(product)
    
    # Add co-occurrence based recommendations
    for product, count in cooccurrence_recs:
        all_recommendations.add(product)
    
    # Convert to list and limit to top_k
    recommendations = list(all_recommendations)[:top_k]
    
    # Generate pricing suggestions based on product performance
    pricing_suggestions = {}
    for product in recommendations:
        stats = product_stats.get(product, {})
        avg_revenue = stats.get("revenue", 0) / max(stats.get("count", 1), 1)
        
        if avg_revenue > 50:
            pricing_suggestions[product] = "Premium product - consider premium bundle pricing"
        elif avg_revenue > 20:
            pricing_suggestions[product] = "Popular item - offer 5% bundle discount"
        else:
            pricing_suggestions[product] = "Value item - consider 10% volume discount"
    
    return {
        "recommendations": recommendations,
        "pricing_suggestions": pricing_suggestions,
        "analysis": {
            "total_products": len(product_stats),
            "top_revenue_product": max(product_stats.keys(), key=lambda p: product_stats[p]["revenue"]) if product_stats else None,
            "most_frequent_product": max(product_stats.keys(), key=lambda p: product_stats[p]["count"]) if product_stats else None
        }
    }
