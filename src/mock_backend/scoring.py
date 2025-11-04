import numpy as np
import pandas as pd
from mock import chatbot_response
from pathlib import Path
from sentence_transformers import SentenceTransformer


EMB_DIR = Path("embeddings")
model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D numpy arrays. Returns float in [-1, 1]."""
    if a is None or b is None:
        return 0.0
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def similarity(response):
    resp, embed_ind = response
    # embedding_matrix = pd.read_pickle(EMB_DIR / "all_embeddings.pkl")
    # doc_embed = embedding_matrix.iloc[embed_ind].values[embed_ind]
    # Load two doc embeddings and take their mean
    docs_dir = Path("embeddings")
    doc0 = np.load(docs_dir / "nhsdoc2_0.npy")
    doc1 = np.load(docs_dir / "nhsdoc2_1.npy")
    doc_embed = ((doc0.astype('float32') + doc1.astype('float32')) / 2.0).astype('float32')

    print(doc_embed.shape)
    for response, _ in resp:
        resp_embed = model.encode([response], convert_to_numpy=True, normalize_embeddings=True).astype('float32')
        sim = cosine_sim(resp_embed,doc_embed)
        resp[response] = sim 

    return resp


def main():
    response_obj = chatbot_response("What are the symptoms of dyslexia")
    resp = similarity(response_obj)
    print(resp)


if __name__ == "__main__":
    main()