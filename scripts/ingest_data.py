import os

# Configure model storage location on D: drive
MODEL_CACHE_DIR = r"D:\Project\HTS AI Agent\models"
os.environ['HF_HOME'] = MODEL_CACHE_DIR
os.environ['TRANSFORMERS_CACHE'] = os.path.join(MODEL_CACHE_DIR, "hub")
os.environ['SENTENCE_TRANSFORMERS_HOME'] = os.path.join(MODEL_CACHE_DIR, "sentence-transformers")

# Create model directories if they don't exist
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)

# Now import the libraries (after setting environment variables)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Paths
PDF_PATH = "data/general_notes/general_notes.pdf"
VECTOR_STORE_PATH = "data/vector_store"

def embed_in_batches(embedding_model, chunks, batch_size=64):
    all_embeddings = []
    texts = [doc.page_content for doc in chunks]
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = embedding_model.embed_documents(batch)
        all_embeddings.extend(batch_embeddings)
    return all_embeddings

def ingest_general_notes():
    print("Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print("Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    print("Loading embedding model...")
    print(f"Models will be stored at: {MODEL_CACHE_DIR}")
    
    # Explicitly set cache folder for the embedding model
    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        cache_folder=MODEL_CACHE_DIR
    )

    print("Embedding chunks and building FAISS vector store...")
    vector_store = FAISS.from_texts(
        texts=[t.page_content for t in texts],
        embedding=embedding_model,
        metadatas=[t.metadata for t in texts]
    )

    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    vector_store.save_local(VECTOR_STORE_PATH)
    print(f"FAISS vector store saved to {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    os.makedirs("data/general_notes", exist_ok=True)
    os.makedirs("data/vector_store", exist_ok=True)
    
    # Print cache locations for verification
    print("Cache Configuration:")
    print(f"HF_HOME: {os.environ.get('HF_HOME')}")
    print(f"TRANSFORMERS_CACHE: {os.environ.get('TRANSFORMERS_CACHE')}")
    print(f"SENTENCE_TRANSFORMERS_HOME: {os.environ.get('SENTENCE_TRANSFORMERS_HOME')}")
    print("-" * 50)
    
    ingest_general_notes()