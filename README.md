# NexSearch: Gemini-Powered Semantic Search Engine

**NexSearch** is a production-grade prototype of a semantic search system designed for e-commerce platforms like Daraz. Unlike traditional keyword-based search, NexSearch understands the **conceptual meaning** of user queries using high-dimensional vector embeddings.

## 🚀 Key Features
- **Semantic Understanding**: Finds "heaters" and "blankets" when a user searches for "something for a cold night."
- **Gemini Embeddings**: Powered by Google's `gemini-embedding-001` (3072-D vectors).
- **Qdrant Vector Database**: Production-ready vector storage and similarity search.
- **Adaptive Retry**: Built-in handling for Gemini API rate limits (429 errors).
- **Synthetic Data**: Includes 100+ diverse product entries across Electronics, Fashion, Home Decor, and Skincare.

## 🛠️ Tech Stack
- **AI/LLM**: Google Gemini (Vertex AI/AI Studio)
- **Vector DB**: Qdrant
- **Logic**: Python 3.12, NumPy
- **Environment**: Dotenv for secure configuration

## 📦 Project Structure
- `main_qdrant.py`: Main entry point for the Qdrant-powered search.
- `qdrant_manager.py`: Logic for collection management and vector search.
- `embedding_engine.py`: Wrapper for generating Gemini embeddings with retry logic.
- `data_generator.py`: Script to generate synthetic product data.
- `.env.example`: Template for environment variables.

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nexsearch.git
cd nexsearch
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Copy `.env.example` to `.env` and add your Gemini API Key:
```powershell
cp .env.example .env
```
Edit `.env` and add your `GOOGLE_API_KEY`.

### 4. Run Qdrant (Required for Dashboard)
To see your embeddings in the browser dashboard, run Qdrant via Docker:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## 🚀 Usage
Run the main semantic search demo:
```bash
python main_qdrant.py
```

### Example Queries:
- **Abstract**: "something warm for cold nights"
- **Category**: "premium luxury skincare for organic glow"
- **Specific**: "iPhone 15 Pro Max"

## 📊 Dashboard View
Once the script is running and Qdrant is active, visit:
👉 **[http://localhost:6333/dashboard](http://localhost:6333/dashboard)**

## 🛡️ License
Distributed under the MIT License.
