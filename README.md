# News Similarity Search

This monorepo contains two separate repos for searching news article similarity:

1. **AWS**
2. **Streamlit**

---

## 1. AWS (FastAPI + Docker)

The AWS folder holds a FastAPI-based API for similarity search using FAISS and SentenceTransformers.

### Features

- **Endpoint**:
  - **HTML UI**: `/search` (web form)
  - **JSON API**: `/api/search` (GET & POST)
- **Data**: `Articles.csv` (2,692 articles) with columns: `Article`, `Date`, `Heading`, `NewsType`.
- **Model**: Sentence embeddings from `all-MiniLM-L6-v2`, indexed in FAISS.

### Status

> Not yet deployed

### Running Locally (with Docker)

1. **Clone the monorepo**:
   ```bash
   git clone <your-repo-url>
   cd News-Similarity-API/AWS
   ```
2. **Place data files** (in `AWS/`):
   - `Articles.csv`
   - Optional: `index.faiss`, `metadata.json`

3. **Build the Docker image** (may take up to 20 minutes for model download and indexing):
   ```bash
   docker build -t news-api .
   ```

4. **Run the container** (starts on port 7860):
   ```bash
   docker run -p 7860:7860 news-api
   ```

5. **Access the service**:
   - Web UI: `http://localhost:7860/`
   - Search form: `http://localhost:7860/search`
   - JSON API: `http://localhost:7860/api/search?q=your+query&top_k=5`

6. **Stop**:
   ```bash
   ctrl + C
   ```

### Running Locally (without Docker)

If dependencies are installed in your environment, simply:

```bash
cd news-similarity/AWS
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```

---

## 2. Streamlit

The Streamlit folder contains an interactive app wrapping the same similarity search logic.

### Live Demo

[https://e3ygzgdzgxkpydoc9wmtvg.streamlit.app/](https://e3ygzgdzgxkpydoc9wmtvg.streamlit.app/)

### Features

- Sidebar inputs: query text and number of results (top_k).
- Real-time search with FAISS & SentenceTransformer.
- Cached index for fast startup.

### Running Locally

1. **Clone the monorepo**:
   ```bash
   git clone <your-repo-url>
   cd News-Similarity-API/Streamlit
   ```
2. **Place data files** (in `Streamlit/`):
   - `Articles.csv`
   - Optional: `index.faiss`, `metadata.json`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open**: `http://localhost:8501`

---

## Common Notes

- **Precomputed Index**: To speed up startup, include `index.faiss` and `metadata.json` alongside `Articles.csv`.
- **Large Model**: Downloading and embedding ~2,700 articles takes time and memory—expect up to 15 minutes on first run.
- **Requirements**:
  - Python 3.8+
  - `sentence-transformers`
  - `faiss-cpu`
  - `pandas`, `numpy`, `streamlit` (for Streamlit folder)
  - `fastapi`, `uvicorn` (for AWS folder)

---
