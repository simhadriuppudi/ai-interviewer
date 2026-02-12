from sentence_transformers import SentenceTransformer

# Initialize model once
# This will download the model on first run if not present
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str) -> list[float]:
    """Generate embedding for a given text."""
    try:
        return model.encode(text).tolist()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
