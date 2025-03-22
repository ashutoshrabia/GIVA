from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict
import uvicorn


app = FastAPI(
    title="News Article Similarity Search API",
    description="API for finding similar news articles",
    version="1.0.0"
)

# Defining a simple data model for our POST endpoint
class SearchQuery(BaseModel):
    query: str  
    top_k: int = 5  


class DocumentStore:
    def __init__(self, csv_path: str = "Articles.csv"):
        # Using a pre-trained model to turn text into vectors (embeddings)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  
        self.index = faiss.IndexFlatL2(self.dimension)  # FAISS index for fast similarity search
        self.documents = []  
        self.load_csv(csv_path)  

    def load_csv(self, csv_path: str):
        # Reading the CSV file where our articles live
        df = pd.read_csv(csv_path, encoding='latin1')  
        # Making sure the CSV has the columns we need
        required_columns = ['Article', 'Date', 'Heading', 'NewsType']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Hey, the CSV needs Article, Date, Heading, and NewsType columns!")
        
      
        articles = df['Article'].astype(str).tolist()
        # Converting articles to embeddings (vectors) so we can compare them later
        embeddings = self.model.encode(articles, show_progress_bar=True) 
        self.index.add(embeddings)  # Adding these vectors to our FAISS index for searching
        
        for idx, row in df.iterrows():
            self.documents.append({
                'id': idx,  
                'article': str(row['Article']),
                'date': str(row['Date']),
                'heading': str(row['Heading']),
                'news_type': str(row['NewsType'])
            })

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        # Turning the user's query into a vector
        query_embedding = self.model.encode([query])[0]
        # Searching the FAISS index for the top_k closest vectors
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        results = []
        # Looping through the results to build our response
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1 and idx < len(self.documents):  
                doc = self.documents[idx]
              
                similarity = 1 - (dist / 2)  
                results.append({
                    'id': doc['id'],
                    'article': doc['article'],
                    'date': doc['date'],
                    'heading': doc['heading'],
                    'news_type': doc['news_type'],
                    'similarity': float(similarity) 
                })
        return results

# Creating our document store 
doc_store = DocumentStore()

def get_styles():
    return """
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }
        .container { max-width: 800px; margin: 50px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h1 { color: #333; }
        a { text-decoration: none; color: #007BFF; }
        a:hover { text-decoration: underline; }
        ul { list-style-type: none; padding: 0; }
        li { background: #fff; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 0 5px rgba(0, 0, 0, 0.1); text-align: left; }
        .search-box { margin: 20px 0; }
        input[type="text"], input[type="number"] { padding: 10px; width: 70%; border: 1px solid #ccc; border-radius: 5px; }
        input[type="submit"] { padding: 10px 20px; border: none; background: #007BFF; color: white; border-radius: 5px; cursor: pointer; }
        input[type="submit"]:hover { background: #0056b3; }
    </style>
    """

#  homepage
@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <html>
        <head><title>News Article Similarity Search</title>{get_styles()}</head>
        <body>
            <div class="container">
                <h1>Welcome to News Article Similarity Search API</h1>
                <p>Go to <a href="/search">search</a> to try a search.</p>
                <p>Or use the <a href="/docs">API Docs</a> for POST requests.</p>
            </div>
        </body>
    </html>
    """

@app.get("/search", response_class=HTMLResponse)
async def search_form(request: Request, query: str = "", top_k: int = 5):
    if not query:  
        return f"""
        <html>
            <head><title>Search Articles</title>{get_styles()}</head>
            <body>
                <div class="container">
                    <h1>Search Articles</h1>
                    <form method="get" class="search-box">
                        <input type="text" name="query" placeholder="Enter search query" required>
                        <input type="number" name="top_k" value="5" min="1" max="10">
                        <input type="submit" value="Search">
                    </form>
                </div>
            </body>
        </html>
        """

    results = doc_store.search(query, top_k)
    html_content = f"""
    <html>
        <head><title>Search Results</title>{get_styles()}</head>
        <body>
            <div class="container">
                <h1>Search Results for "{query}"</h1>
                <p><a href="/search">New Search</a></p>
                <ul>
    """
    
    for result in results:
        html_content += f"""
            <li>
                <strong>{result['heading']}</strong> ({result['date']}) - {result['news_type']}<br>
                <em>Similarity: {result['similarity']:.2f}</em><br>
                {result['article'][:200]}...  <!-- Cutting it short so it’s not overwhelming -->
            </li>
        """
    html_content += """</ul></div></body></html>"""
    return HTMLResponse(content=html_content)

# The POST endpoint for programmatic API access
@app.post("/api/search")
async def search_documents(query: SearchQuery):
    # Just grab the results and send them back as JSON
    results = doc_store.search(query=query.query, top_k=query.top_k)
    return {"results": results}

# Added a GET endpoint to match the exact requirement
@app.get("/api/search")
async def search_documents_get(q: str, top_k: int = 5):
   
    results = doc_store.search(query=q, top_k=top_k)
    return {"results": results}

# Start the server when we run the file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)  