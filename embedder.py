import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest

def embed_and_store():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading chunks...")
    chunks = ingest()

    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete collection if it exists to avoid duplicates
    try:
        client.delete_collection("professor_reviews")
    except:
        pass
    
    collection = client.create_collection("professor_reviews")

    print(f"Embedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    ids = [f"{chunk['source']}_{chunk['chunk_index']}" for chunk in chunks]

    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )

    print(f"Done! {len(chunks)} chunks stored in ChromaDB.")

if __name__ == "__main__":
    embed_and_store()