import google.generativeai as genai
import numpy as np
import os
import json
import time
from typing import List, Dict, Optional

class EmbeddingEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            # We don't raise error here because it might be provided later or 
            # hardcoded for local-only use, but we recommend env variables.
            pass
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = "models/gemini-embedding-001"

    def get_embedding(self, text: str, retries: int = 3) -> List[float]:
        """Generate an embedding for a single text string with simple retry."""
        for attempt in range(retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type="retrieval_document",
                    title="Product Description"
                )
                return result['embedding']
            except Exception as e:
                if "429" in str(e) and attempt < retries - 1:
                    print(f"Rate limited. Retrying in 5 seconds... (Attempt {attempt+1}/{retries})")
                    time.sleep(5)
                    continue
                print(f"Error generating embedding: {e}")
                return []
        return []

    def get_embeddings_batch(self, texts: List[str], retries: int = 3) -> List[List[float]]:
        """Generate embeddings for a batch of text strings with simple retry."""
        for attempt in range(retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=texts,
                    task_type="retrieval_document"
                )
                return result['embedding']
            except Exception as e:
                if "429" in str(e) and attempt < retries - 1:
                    print(f"Rate limited. Retrying in 5 seconds... (Attempt {attempt+1}/{retries})")
                    time.sleep(5)
                    continue
                print(f"Error generating batch embeddings: {e}")
                return []
        return []

    def embed_products(self, products: List[Dict]) -> List[Dict]:
        """Adds an 'embedding' field to each product using name and description."""
        texts = [f"{p['name']} {p['description']}" for p in products]
        
        # Batch size for Gemini embeddings is typically 100
        batch_size = 50
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_embeddings = self.get_embeddings_batch(batch)
            if batch_embeddings:
                embeddings.extend(batch_embeddings)
            else:
                # Handle failure by adding None or skipping
                embeddings.extend([None] * len(batch))
        
        for i, product in enumerate(products):
            if i < len(embeddings):
                product['embedding'] = embeddings[i]
                
        return products

if __name__ == "__main__":
    # Test script
    engine = EmbeddingEngine()
    test_text = "Wireless headphones with noise cancellation"
    emb = engine.get_embedding(test_text)
    print(f"Embedding size: {len(emb)}")
    print(f"Sample: {emb[:5]}")
