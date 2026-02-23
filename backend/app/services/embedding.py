from sentence_transformers import SentenceTransformer

# Lazy initialization - model loads on first use, not at import time
# This prevents startup hangs on cloud deployments
_model = None

def _get_model():
    """Get or initialize the embedding model (lazy loading)"""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def get_embedding(text: str) -> list[float]:
    """Generate embedding for a given text."""
    try:
        model = _get_model()
        return model.encode(text).tolist()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
