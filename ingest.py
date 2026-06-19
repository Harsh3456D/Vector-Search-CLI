import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

def run_ingestion():
    print("Booting up Local Instance for Qdrant Database")
    client = QdrantClient(path="./qdrant_db")
    COLLECTION_NAME = "my_notes"
    client.create_collection(
        collection_name= COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    print(f"Collection '{COLLECTION_NAME}' created successfully")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"Model is successfully Loaded")

    NOTES_DIR = "./notes"
    if not os.path.exists(NOTES_DIR) or not os.listdir(NOTES_DIR):
        print(f"Error : The directory doesn't exist")
        return client, COLLECTION_NAME
    
    points = []
    point_id = 1

    print("Reading Notes and generating Vectors")
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(NOTES_DIR, filename)

            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()

            chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
            
            for chunk_index, chunk_text in enumerate(chunks):
                vector = model.encode(chunk_text).tolist()

                point = PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "source_file": filename,
                        "chuck_index": chunk_index,
                        "text": chunk_text
                    }
                )
                points.append(point)
                point_id += 1

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Successfully Ingested {len(points)} text into chunks into the vector database")
    else:
        print("No Text found for ingestion")

    return client, COLLECTION_NAME

if __name__ == "__main__":
    run_ingestion()