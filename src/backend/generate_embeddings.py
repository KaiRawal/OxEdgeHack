import os
import pickle
import numpy as np
from pathlib import Path
import faiss
from transformers import AutoTokenizer, AutoModel
import torch

# Initialize embedding model
print("Loading embedding model...")
tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")
model.eval()

def embed_text(text):
    """Generate embeddings using ModernBERT"""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
    return embeddings.numpy()[0]

def generate_embeddings():
    docs_dir = Path("docs")
    embeddings_dir = Path("embeddings")
    embeddings_dir.mkdir(exist_ok=True)

    if not docs_dir.exists():
        print("Error: docs/ directory not found!")
        return

    documents = []
    embeddings = []
    filenames = []

    for file_path in docs_dir.glob("*.txt"):
        print(f"Processing {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            filenames.append(file_path.name)
            embeddings.append(embed_text(content))

    if not documents:
        print("No .txt files found in docs/")
        return

    embeddings_array = np.array(embeddings).astype('float32')

    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings_array)

    faiss.write_index(index, str(embeddings_dir / "faiss_index.bin"))
    with open(embeddings_dir / "documents.pkl", "wb") as f:
        pickle.dump(documents, f)
    with open(embeddings_dir / "filenames.pkl", "wb") as f:
        pickle.dump(filenames, f)

    print(f"\n✅ Successfully created embeddings for {len(documents)} documents!")

if __name__ == "__main__":
    generate_embeddings()
