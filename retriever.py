import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("professor_reviews")

def retrieve(query, k=4):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    test_queries = [
        "What do students say about Dr. Mylavarapu's exams?",
        "Does Hong Sung give tests in his classes?",
        "How is Michael Bihn's teaching style?"
    ]
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        results = retrieve(query)
        for r in results:
            print(f"Source: {r['source']} | Distance: {r['distance']:.3f}")
            print(f"{r['text'][:150]}...")
            print()