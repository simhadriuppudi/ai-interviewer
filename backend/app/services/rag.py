import numpy as np
import os
import pickle
from backend.app.services.embedding import get_embedding

class RAGService:
    def __init__(self, storage_path="vector_store/index.faiss", doc_path="vector_store/docs.pkl"):
        import faiss  # lazy import - only loads when RAGService is first used
        self.dimension = 384 # All-MiniLM-L6-v2
        self.storage_path = storage_path
        self.doc_path = doc_path
        self.documents = []
        
        if os.path.exists(storage_path) and os.path.exists(doc_path):
            self.index = faiss.read_index(storage_path)
            with open(doc_path, "rb") as f:
                self.documents = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
    
    def add_document(self, text: str, chunk_size: int = 500):
        if not text:
            return
            
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        embeddings = []
        
        for chunk in chunks:
            emb = get_embedding(chunk)
            if emb:
                embeddings.append(emb)
                self.documents.append(chunk)
        
        if embeddings:
            self.index.add(np.array(embeddings).astype('float32'))
            self.save()

    def search(self, query: str, k: int = 3) -> list[str]:
        if self.index.ntotal == 0:
            return []
            
        query_vector = get_embedding(query)
        if not query_vector:
            return []
            
        D, I = self.index.search(np.array([query_vector]).astype('float32'), k)
        results = []
        for i in I[0]:
            if i != -1 and i < len(self.documents):
                results.append(self.documents[i])
        return results

    def save(self):
        import faiss  # lazy import
        if not os.path.exists("vector_store"):
            os.makedirs("vector_store")
        faiss.write_index(self.index, self.storage_path)
        with open(self.doc_path, "wb") as f:
            pickle.dump(self.documents, f)

    def clear(self):
        import faiss  # lazy import
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.save()

# Lazy singleton - only created when first accessed, NOT at import time
_rag_engine = None

def get_rag_engine() -> RAGService:
    """Get or create the RAG engine (lazy initialization)."""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGService()
    return _rag_engine

# Keep backward compatibility - but now lazy
rag_engine = None  # Will be set on first use via get_rag_engine()
