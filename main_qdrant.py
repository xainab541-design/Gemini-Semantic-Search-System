import json
import os
import time
from data_generator import generate_products
from embedding_engine import EmbeddingEngine
from qdrant_manager import QdrantManager

def load_or_generate_data(engine, force_regen=False):
    """Generate product data and pre-compute embeddings."""
    data_file = "products_with_embeddings.json"
    
    if os.path.exists(data_file) and not force_regen:
        print(f"Loading existing data and embeddings from {data_file}")
        with open(data_file, "r") as f:
            return json.load(f)
            
    print("Generating synthetic data (120 products)...")
    products = generate_products(120)
    
    print("Generating embeddings using Gemini API (this may take a minute)...")
    products_with_embeddings = engine.embed_products(products)
    
    with open(data_file, "w") as f:
        json.dump(products_with_embeddings, f, indent=4)
        
    print(f"Data saved to {data_file}")
    return products_with_embeddings

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        return
        
    try:
        # 1. Initialize Engines
        # Use env variables for Qdrant connection if available (for Dashboard access)
        qdrant_url = os.getenv("QDRANT_URL") 
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        engine = EmbeddingEngine(api_key=api_key)
        q_manager = QdrantManager(
            collection_name="daraz_products", 
            vector_size=3072, 
            url=qdrant_url, 
            api_key=qdrant_api_key
        )
        
        # 2. Load or Generate Product Data
        products_data = load_or_generate_data(engine)
        
        # 3. Upsert to Qdrant
        print("\nIndexing products into Qdrant...")
        q_manager.upsert_products(products_data)
        
        print("\n" + "="*40)
        print(" 🚀 SEMANTIC SEARCH READY (POWERED BY QDRANT) ")
        print("="*40)
        
        test_queries = [
            "iPhone 15 Pro Max",
            "something for a cold night",
            "premium luxury skincare for organic glow"
        ]
        
        for query in test_queries:
            print(f"\n[QUERY] '{query}'")
            
            # Embed the query
            query_vector = engine.get_embedding(query)
            
            if not query_vector:
                print("  Failed to embed query.")
                continue
                
            # Search in Qdrant
            results = q_manager.search(query_vector, top_k=3)
            
            for i, res in enumerate(results):
                print(f"  {i+1}. {res['name']} ({res['category']})")
                print(f"     Price: ${res['price']} | Qdrant Score: {res['similarity_score']:.4f}")
                print(f"     Description: {res['description'][:100]}...")
                
        print("\n" + "-"*40)
        print("Interactive Search Session:")
        while True:
            user_query = input("\nTry your search (or 'q' to exit): ")
            if user_query.lower() == 'q':
                break
                
            query_vector = engine.get_embedding(user_query)
            if query_vector:
                results = q_manager.search(query_vector, top_k=5)
                print(f"\nFound {len(results)} matches for '{user_query}' in Qdrant:")
                for i, res in enumerate(results):
                    print(f"  {i+1}. {res['name']} | Category: {res['category']} | Score: {res['similarity_score']:.4f}")
                    print(f"     - {res['description']}")
            else:
                print("Could not generate embedding for query.")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
