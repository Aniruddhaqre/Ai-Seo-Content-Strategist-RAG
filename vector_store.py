import json
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Initialize the Local Embedding Model
# This will download the model once (~80MB) and then run locally.
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize ChromaDB in Persistent Mode
# This saves your data to a folder called 'my_local_db'
client = chromadb.PersistentClient(path="./my_local_db")
collection = client.get_or_create_collection(name="ayurveda_gap_analysis")

def upload_to_local_db(json_file, business_label):
    with open(json_file, 'r') as f:
        chunks = json.load(f)

    print(f"Embedding {len(chunks)} chunks for {business_label}...")

    # We process in small batches to be kind to your RAM
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        
        # Extract data for Chroma
        ids = [c['chunk_id'] for c in batch]
        texts = [c['chunk_content'] for c in batch]
        
        # Generate Embeddings Locally
        embeddings = model.encode(texts).tolist()
        
        # Prepare Metadata (Chroma requires flat dictionaries)
        metadatas = []
        for c in batch:
            metadatas.append({
                "source": business_label,
                "url": c['url'],
                "page_id": c['page_id']
            })

        # Add to local DB
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        print(f"Done: {i + len(batch)} / {len(chunks)}")

# Run it
upload_to_local_db("my_business_clean_chunks.json", "Self")
# upload_to_local_db("competitor_chunks.json", "Comp1")