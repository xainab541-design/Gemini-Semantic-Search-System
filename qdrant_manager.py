from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any, Optional
import uuid

class QdrantManager:
    def __init__(self, collection_name: str = "products", vector_size: int = 3072, url: Optional[str] = None, api_key: Optional[str] = None):
        # If URL is provided, connect to external server. Otherwise, use local memory.
        if url:
            print(f"Connecting to Qdrant at {url}...")
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            print("Using local in-memory Qdrant storage.")
            self.client = QdrantClient(":memory:")
            
        self.collection_name = collection_name
        self.vector_size = vector_size
        self._initialize_collection()

    def _initialize_collection(self):
        """Create a collection if it doesn't already exist."""
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            print(f"Creating Qdrant collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

    def upsert_products(self, products: List[Dict[str, Any]]):
        """Upload product embeddings and metadata to Qdrant."""
        points = []
        for product in products:
            if not product.get("embedding"):
                continue
            
            # Extract metadata (convert list to dict if needed for storage)
            payload = {
                "name": product["name"],
                "category": product["category"],
                "description": product["description"],
                "price": product["price"],
                "metadata": product["metadata"]
            }
            
            points.append(PointStruct(
                id=str(uuid.uuid4()), # Unique ID for Qdrant
                vector=product["embedding"],
                payload=payload
            ))
            
        if points:
            print(f"Upserting {len(points)} points to Qdrant...")
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Perform vector search in Qdrant."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        # Format results for consistent output
        results = []
        for hit in search_result:
            product = hit.payload
            product["similarity_score"] = hit.score
            results.append(product)
            
        return results

if __name__ == "__main__":
    # Quick test
    manager = QdrantManager(vector_size=3)
    test_products = [
        {"name": "Heater", "category": "Home", "description": "Warm", "price": 50, "metadata": [], "embedding": [0.1, 0.2, 0.3]},
        {"name": "Ice Cream", "category": "Food", "description": "Cold", "price": 5, "metadata": [], "embedding": [-0.1, -0.2, -0.3]}
    ]
    manager.upsert_products(test_products)
    
    results = manager.search([0.1, 0.2, 0.3], top_k=1)
    print(f"Top Qdrant result: {results[0]['name']} (Score: {results[0]['similarity_score']:.4f})")
