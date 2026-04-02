import json
import random
import uuid

def generate_products(count=120):
    categories = {
        "Electronics": {
            "products": ["Smartphone", "Laptop", "Wireless Headphones", "Smartwatch", "Bluetooth Speaker", "Tablet", "Gaming Console", "Mechanical Keyboard", "Monitor", "VR Headset"],
            "features": ["High-performance", "Sleek design", "Long battery life", "4K resolution", "Fast charging", "Noise-cancelling", "Water-resistant"],
            "metadata": ["gadget", "tech", "portable", "electronics"]
        },
        "Fashion": {
            "products": ["Denim Jacket", "Cotton T-shirt", "Leather Boots", "Silk Scarf", "Running Shoes", "Winter Parka", "Linen Trousers", "Sunglasses", "Hoodie", "Sportswear Set"],
            "features": ["Breathable", "Sustainable", "Premium quality", "Modern fit", "Durable", "Lightweight", "Comfortable"],
            "metadata": ["apparel", "clothing", "style", "fashion"]
        },
        "Home Decor": {
            "products": ["Ceramic Vase", "Plush Blanket", "Table Lamp", "Wall Art", "Scented Candle", "Area Rug", "Throw Pillow", "Bookshelf", "Wall Clock", "Indoor Plant Pot"],
            "features": ["Minimalist", "Cozy", "Handcrafted", "Elegant", "Artisan", "Modern", "Vintage"],
            "metadata": ["interior", "home", "living", "decor"]
        },
        "Skincare": {
            "products": ["Hydrating Serum", "Moisturizing Cream", "Sunscreen SPF 50", "Facial Cleanser", "Exfoliating Scrub", "Night Repair Oil", "Vitamin C Toner", "Sheet Mask", "Eye Cream", "Lip Balm"],
            "features": ["Organic", "Dermatologist tested", "Fragrance-free", "Glow-enhancing", "Anti-aging", "Nourishing", "Vegan"],
            "metadata": ["beauty", "self-care", "glow", "skincare"]
        }
    }

    products = []
    
    # Add specific "Edge Case" products to ensure the search range
    edge_cases = [
        {
            "product_id": str(uuid.uuid4()),
            "name": "Arctic Comfort Electric Heater",
            "category": "Home Decor",
            "description": "A powerful electric heater designed to keep your room warm and cozy during the coldest nights. Features adjustable temperature settings and a safety auto-off function.",
            "price": 89.99,
            "metadata": ["cozy", "warmth", "winter", "portable"]
        },
        {
            "product_id": str(uuid.uuid4()),
            "name": "CloudNine Weighted Blanket",
            "category": "Home Decor",
            "description": "Experience deeper sleep with this heavy weighted blanket. Perfect for staying warm on a cold night or relaxing after a long day.",
            "price": 120.00,
            "metadata": ["comfort", "warm", "sleep", "heavy"]
        },
        {
            "product_id": str(uuid.uuid4()),
            "name": "Ultra-Soft Fleece Hoodie",
            "category": "Fashion",
            "description": "Stay warm in style with our premium fleece hoodie. Double-lined for extra warmth, making it the perfect companion for a chilly evening.",
            "price": 45.50,
            "metadata": ["casual", "warm", "winter", "fashion"]
        }
    ]
    products.extend(edge_cases)

    for i in range(count - len(edge_cases)):
        cat_name = random.choice(list(categories.keys()))
        cat_data = categories[cat_name]
        
        prod_name = f"{random.choice(cat_data['features'])} {random.choice(cat_data['products'])}"
        description = f"This {prod_name} is designed for anyone looking for {random.choice(cat_data['features']).lower()} functionality. " \
                      f"Ideal for {cat_name.lower()} enthusiasts, it offers a {random.choice(cat_data['features']).lower()} experience like no other."
        
        price = round(random.uniform(10, 2000), 2)
        metadata = random.sample(cat_data['metadata'], k=2)
        if price > 500:
            metadata.append("luxury")
        
        products.append({
            "product_id": str(uuid.uuid4()),
            "name": prod_name,
            "category": cat_name,
            "description": description,
            "price": price,
            "metadata": metadata
        })

    return products

if __name__ == "__main__":
    data = generate_products(120)
    with open("products.json", "w") as f:
        json.dump(data, f, indent=4)
    print(f"Generated {len(data)} products in products.json")
