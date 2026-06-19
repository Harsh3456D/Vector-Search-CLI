from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

def semantic_search():
    client = QdrantClient(path="./qdrant_db")
    COLLECTION_NAME = "my_notes"

    print("loading embedding model")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("\n---Semantic Note Search Engine Initialized ---")
    print("Type 'exit' to Quit the program")

    while True:
        query = input("Enter your search query: ").strip()
        if query.lower() == 'exit':
            print("Program Ended")
            break
        
        if not query:
            continue

        query_vector = model.encode(query).tolist()

        query_response = client.query_points(
            collection_name = COLLECTION_NAME,
            query = query_vector,
            limit=3
        )

        search_results = query_response.points

        print(f"\nTop Matches for =: '{query}'")
        print("=" * 50)

        if not search_results:
            print("No matching notes found")

        for index, hit in enumerate(search_results, 1):
            score = hit.score
            text = hit.payload["text"]
            source = hit.payload["source_file"]

            print(f"Match #{index} [confidence Score: {score:.4f}] [Source:{source}]")
            print(f"Content: {text}")
            print("-" * 50)
        print("/n")

if __name__ == "__main__":
    semantic_search()