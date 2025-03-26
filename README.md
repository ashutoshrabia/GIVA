# GIVA News Similarity API

This is a FastAPI-based API that searches for similar news articles based on a user-provided query. It uses sentence embeddings from the `all-MiniLM-L6-v2` model (via `sentence-transformers`) and FAISS for efficient similarity search. 

## Approach
- **Data**: The API uses a CSV file (`Articles.csv`) containing 2692 news articles with columns: `Article`, `Date`, `Heading`, and `NewsType`. This data is loaded into memory for embedding generation and can be imported into a Postgres database (e.g., Supabase) for persistent storage.
- **Embedding**: Articles are converted to vector embeddings using `sentence-transformers` (`all-MiniLM-L6-v2`), which are indexed with FAISS for fast similarity search.
- **API**: Built with FastAPI, it offers:
  - A web interface (`/search`) for HTML-based search.
  - JSON endpoints (`/api/search`) for programmatic access (GET and POST).
- **Challenges**:
  - Encountered an ImportError: cannot import name `cached_download` from `huggingface_hub` due to a version mismatch. `sentence-transformers==2.2.2` expects huggingface_hub versions with cached_download `(e.g., 0.10.1)`, but a newer version `(0.23.4)` was installed. Resolved by downgrading to `huggingface_hub==0.10.1` in `requirements.txt`.
  - Faced multiple runtime errors during deployment on Hugging Face Spaces, including:
    - PermissionError: `[Errno 13] Permission denied`: '/.cache': The container user lacked write access to the default cache directory. Fixed by setting `HF_HOME=/app/cache` and ensuring the directory is writable with `chmod` 
      R 777 /app/cache.
    - PermissionError: `[Errno 13] Permission denied`: '/app/cache/token': huggingface_hub couldn’t write a token file. 
  - Attempted deployment on Render, but hit an out-of-memory error because the app exceeded the free tier’s 512 MB RAM limit while loading the model and encoding articles.
## Steps to Run Locally
### Prerequisites
- Docker installed ([Download](https://www.docker.com/get-started))
- `Articles.csv` with columns: `Article`, `Date`, `Heading`, `NewsType`

### Steps
1. **Clone the Repository** (or copy files to a `GIVA` directory):
   ```bash
   git clone <your-repo-url>  # If hosted on Git/HF
   cd GIVA
2. **Build the docker Image** (this can take upto 20 minutes) :
   ```bash
   docker build -t giva-news-api .
3. **Run the container** (this can take upto 5 minutes) :
   ```bash
   docker run -p 7860:7860 giva-news-api
4. **Access the API** :
   - Open http://localhost:7860/ in your browser for the welcome page.
   - Use /search or /api/search endpoints
5. **Stop the container** :
   - Press ctrl + c  
## or if you have installed all requirements in your local , then simply run app.py
## Example API Requests & Responses

### 1. Welcome Page (GET /)
- **Request**: Open in browser or use curl:
  ```bash
  curl http://localhost:7860/
</code></pre>
<html>
    <head>News Article Similarity Search</head>
    <body>
        <div class="container">
            <h1>Welcome to News Article Similarity Search API</h1>
            <p>Go to <a href="/search">search</a> to try a search.</p>
            <p>Or use the <a href="/docs">API Docs</a> for POST requests.</p>
        </div>
    </body>
</html>

### 2. Search form (GET /search)
- **Request**: Browse or curl with query:
  ```bash
  curl "http://localhost:7860/search?query=technology+news&top_k=3"
<html>
    <head>Search Results</head>
    <body>
        <div class="container">
            <h1>Search Results for "technology news"</h1>
            <p><a href="/search">New Search</a></p>
            <ul>
                <li>
                    <strong>Tech Breakthrough</strong> (2023-01-15) - Tech
                    <em>Similarity: 0.92</em>
                    New AI tool released...
                </li>
                <li>
                    <strong>Gadgets Unveiled</strong> (2023-02-10) - Tech
                    <em>Similarity: 0.87</em>
                    Latest smartphones hit the market...
                </li>
                <li>
                    <strong>Tech Trends</strong> (2023-03-05) - Tech
                    <em>Similarity: 0.85</em>
                    Predictions for 2023 tech...
                </li>
            </ul>
        </div>
    </body>
</html>

### 3. JSON API (GET /api/search)
- **Request**: Browse or curl with query:
  ```bash
  curl "http://localhost:7860/api/search?q=technology+news&top_k=3"
```json
{
    "results": [
        {
            "id": 0,
            "article": "New AI tool released...",
            "date": "2023-01-15",
            "heading": "Tech Breakthrough",
            "news_type": "Tech",
            "similarity": 0.92
        },
        {
            "id": 1,
            "article": "Latest smartphones hit the market...",
            "date": "2023-02-10",
            "heading": "Gadgets Unveiled",
            "news_type": "Tech",
            "similarity": 0.87
        },
        {
            "id": 2,
            "article": "Predictions for 2023 tech...",
            "date": "2023-03-05",
            "heading": "Tech Trends",
            "news_type": "Tech",
            "similarity": 0.85
        }
    ]
}
```
### 4. JSON API (POST /api/search)
- **Request**: Browse or curl with query:
  ```bash
  curl -X POST "http://localhost:7860/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "technology news", "top_k": 3}'
  
```json  
{
    "results": [
        {
            "id": 0,
            "article": "New AI tool released...",
            "date": "2023-01-15",
            "heading": "Tech Breakthrough",
            "news_type": "Tech",
            "similarity": 0.92
        },
        {
            "id": 1,
            "article": "Latest smartphones hit the market...",
            "date": "2023-02-10",
            "heading": "Gadgets Unveiled",
            "news_type": "Tech",
            "similarity": 0.87
        },
        {
            "id": 2,
            "article": "Predictions for 2023 tech...",
            "date": "2023-03-05",
            "heading": "Tech Trends",
            "news_type": "Tech",
            "similarity": 0.85
        }
    ]
}
