from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

app = FastAPI(title="AI search API")
print("Starting Server...")
client = QdrantClient(path="./qdrant_db")
model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "my_notes"

class SearchRequest(BaseModel):
    query: str
    limit: int = 3

class SearchResult(BaseModel):
    score: float
    source: str
    text: str

class SearchResponse(BaseModel):
    results: list[SearchResult]

@app.post("./search", response_model=SearchResponse)
async def perform_search(request: SearchRequest):
    try:
        query_vector = model.encode(request.query)

        query_response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=request.limit
        )

        formatted_results = []
        for hit in query_response.points:
            formatted_results.append(
                SearchResult(
                    score=hit.score,
                    source=hit.payload["source_file"],
                    text=hit.payload["text"]
                )
            )
        return SearchResponse(results=formatted_results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    