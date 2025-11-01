import os
from pathlib import Path
import pickle
import numpy as np
import torch
import pandas as pd
import faiss
from transformers import AutoTokenizer, AutoModel

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DOCS_DIR = Path("docs")
EMB_DIR = Path("embeddings")
CHUNKS_DIR = Path("chunks")
MODEL_NAME = "answerdotai/ModernBERT-base"
CHUNK_SIZE = 512
DEVICE = "cpu"

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def load_model():
    print("📌 Loading ModernBERT model (CPU)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    return tokenizer, model


def embed_chunks(text: str, tokenizer, model):
    """Yield tuple: (embedding np.array, chunk_text, chunk_index)."""
    tokens = tokenizer(
        text,
        return_tensors="pt",
        truncation=False,
        padding=False
    )

    input_ids = tokens["input_ids"][0]
    num_chunks = (len(input_ids) + CHUNK_SIZE - 1) // CHUNK_SIZE

    with torch.no_grad():
        for i in range(num_chunks):
            chunk_ids = input_ids[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]
            chunk_input = {"input_ids": chunk_ids.unsqueeze(0).to(DEVICE)}

            outputs = model(**chunk_input)
            pooled = outputs.last_hidden_state.mean(dim=1)
            pooled = pooled / pooled.norm(dim=1, keepdim=True)

            # Recover chunk text
            chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)

            yield pooled.cpu().numpy().astype("float32"), chunk_text, i


# ---------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------
def process_documents(tokenizer, model):
    if not DOCS_DIR.exists():
        raise FileNotFoundError("❌ docs/ not found")

    EMB_DIR.mkdir(exist_ok=True)
    CHUNKS_DIR.mkdir(exist_ok=True)

    rows = {}  # index -> embedding row

    files = sorted(DOCS_DIR.glob("*.txt"))
    if not files:
        raise RuntimeError("❌ No .txt files found in docs/")

    print(f"📄 Found {len(files)} documents\n")

    for fidx, file_path in enumerate(files, start=1):
        print(f"➡️ [{fidx}/{len(files)}] {file_path.name}")
        text = file_path.read_text(encoding="utf-8")

        base_name = file_path.stem

        for emb, chunk_text, cidx in embed_chunks(text, tokenizer, model):
            chunk_name = f"{base_name}_{cidx}"

            # Save embedding vector
            np.save(EMB_DIR / f"{chunk_name}.npy", emb)

            # Save chunk text
            (CHUNKS_DIR / f"{chunk_name}.txt").write_text(chunk_text, encoding="utf-8")

            rows[chunk_name] = emb.squeeze()

    return rows


# ---------------------------------------------------------------------
# Save global representation
# ---------------------------------------------------------------------
def save_all_embeddings(rows):
    print("\n💾 Saving combined embedding dataframe...")

    df = pd.DataFrame.from_dict(rows, orient="index")
    df.index.name = "chunk_id"
    df.to_pickle(EMB_DIR / "all_embeddings.pkl")

    print(f"✅ DataFrame saved → {EMB_DIR}/all_embeddings.pkl")
    print(f"📊 Rows: {df.shape[0]}  |  Dimensions: {df.shape[1]}")
    return df


def build_faiss_index():
    print("\n📌 Building FAISS index from combined embeddings...")

    emb_dir = Path("embeddings")
    df_path = emb_dir / "all_embeddings.pkl"
    index_path = emb_dir / "faiss_index.bin"

    if not df_path.exists():
        raise FileNotFoundError("❌ Missing all_embeddings.pkl — run embedding generation first")

    df = pd.read_pickle(df_path)

    # Convert to float32 matrix
    emb_matrix = df.to_numpy().astype("float32")
    dim = emb_matrix.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(emb_matrix)

    faiss.write_index(index, str(index_path))

    print(f"✅ FAISS index created and saved to: {index_path}")
    print(f"📊 Index size: {emb_matrix.shape[0]} vectors | dim = {dim}")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    tokenizer, model = load_model()
    rows = process_documents(tokenizer, model)
    save_all_embeddings(rows)
    build_faiss_index()
    print("\n🎉 ✅ Finished processing all documents!")


if __name__ == "__main__":
    main()
