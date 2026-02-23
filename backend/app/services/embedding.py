# Fully lazy imports - nothing loads until first embedding request
# This prevents PyTorch/sentence-transformers from hanging server startup
_model = None

def _get_model():
    """Lazily import and initialize the embedding model on first use."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # lazy import
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
