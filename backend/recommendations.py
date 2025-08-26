import tensorflow as tf
import tensorflow_recommenders as tfrs
from analysis import get_sales_data
from database import SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import Dict, List
from collections import Counter
from fastapi import Depends

# Define the model with proper TensorFlow Recommenders setup
class RecommendationModel(tfrs.Model):
    def __init__(self, unique_products: List[str]):
        super().__init__()
        self.product_vocabulary = unique_products
        self.product_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=unique_products, mask_token=None),
            tf.keras.layers.Embedding(len(unique_products) + 1, 64),
        ])
        
        # Create candidate embeddings for retrieval
        self.candidate_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=unique_products, mask_token=None),
            tf.keras.layers.Embedding(len(unique_products) + 1, 64),
        ])
        
        # Use retrieval task without problematic metrics
        self.task = tfrs.tasks.Retrieval()
        
    def call(self, features):
        return self.product_model(features["product"])

    def compute_loss(self, features: Dict[str, tf.Tensor], training=False) -> tf.Tensor:
        query_embeddings = self.product_model(features["product"])
        candidate_embeddings = self.candidate_model(features["product"])
        return self.task(query_embeddings, candidate_embeddings)

def get_recommendations(db: Session = Depends(get_db)) -> Dict:
    # Fetch sales data from SQLite
    sales = get_sales_data(db)
    if not sales:
        return {"recommendations": [], "pricing_suggestions": {}}

    # Extract products and count popularity
    products = [sale.product for sale in sales]
    product_counts = Counter(products)
    unique_products = list(set(products))

    # Train TFRS model
    model = RecommendationModel(unique_products)
    tf_dataset = tf.data.Dataset.from_tensor_slices({"product": products})
    tf_dataset = tf_dataset.shuffle(len(products)).batch(32).cache()

    model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))
    model.fit(tf_dataset, epochs=1, verbose=0)

    # Get embeddings for all unique products
    product_embeddings = model({"product": tf.constant(unique_products)})
    
    # Calculate similarity scores and get top recommendations
    similarity_scores = tf.linalg.norm(product_embeddings, axis=1)
    top_indices = tf.nn.top_k(similarity_scores, k=min(3, len(unique_products))).indices
    top_recommendations = [unique_products[i] for i in top_indices.numpy()]

    # Enhanced bundle pricing logic
    pricing_suggestions = {}
    # Count co-occurrences of products in sales (e.g., same day)
    product_pairs = Counter()
    for i in range(len(sales) - 1):
        for j in range(i + 1, len(sales)):
            if sales[i].date == sales[j].date:  # Same day purchase
                pair = tuple(sorted([sales[i].product, sales[j].product]))
                product_pairs[pair] += 1

    for (prod1, prod2), count in product_pairs.most_common(2):  # Top 2 pairs
        if count > 1:
            base_price1 = next((s.amount for s in sales if s.product == prod1), 0)
            base_price2 = next((s.amount for s in sales if s.product == prod2), 0)
            total_price = base_price1 + base_price2
            # Tiered discount: 10% for 2+ occurrences, 15% for 5+
            discount = total_price * (0.15 if count >= 5 else 0.10)
            pricing_suggestions[f"{prod1} + {prod2}"] = f"Bundle price: ${total_price - discount:.2f} (save ${discount:.2f}, {count} times bought together)"

    return {
        "recommendations": top_recommendations,
        "pricing_suggestions": pricing_suggestions
    }