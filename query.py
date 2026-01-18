import chromadb
from sentence_transformers import SentenceTransformer

# --- 1. CONFIGURATION & INITIALIZATION ---

# Point this to your local model folder if you downloaded it manually to avoid internet errors
MODEL_PATH = 'all-MiniLM-L6-v2' 

# Initialize the model (The "Translator")
model = SentenceTransformer(MODEL_PATH)

# Initialize ChromaDB (The "Librarian")
# Point to the SAME folder name you used during upload ('./my_local_db')
client = chromadb.PersistentClient(path="./my_local_db")

# Get the existing collection
collection = client.get_or_create_collection(name="ayurveda_gap_analysis")


def query_ayurveda_db(user_query, n_results=3):
    # 1. Convert search query into a vector (embedding)
    # Important: Use the same model you used for uploading!
    query_embedding = model.encode([user_query]).tolist()

    # 2. Search the collection
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    # 3. Print the results
    print(f"\n--- Results for: '{user_query}' ---")
    for i in range(len(results['ids'][0])):
        content = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]
        
        print(f"\n[Rank {i+1}] Score (Distance): {distance:.4f}")
        print(f"Source: {metadata['source']} | URL: {metadata['url']}")
        print(f"Content: {content[:200]}...") # Showing snippet
        print("-" * 20)

    return results

# Example Usage:
# query_ayurveda_db("What are the benefits of Triphala for digestion?")