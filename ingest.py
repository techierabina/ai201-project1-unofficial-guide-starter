import os

def load_documents(folder="documents"):
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text
            })
    return documents

def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) > 0:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest(folder="documents"):
    documents = load_documents(folder)
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": chunk
            })
    return all_chunks

if __name__ == "__main__":
    chunks = ingest()
    print(f"Total chunks: {len(chunks)}")
    print("\n--- 5 Sample Chunks ---\n")
    for chunk in chunks[:5]:
        print(f"Source: {chunk['source']}")
        print(f"Chunk {chunk['chunk_index']}: {chunk['text']}")
        print("-" * 50)