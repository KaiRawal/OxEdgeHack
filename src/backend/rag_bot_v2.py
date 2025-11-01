import os
import numpy as np
from pathlib import Path
import gradio as gr
import faiss
from transformers import AutoTokenizer, AutoModel
import anthropic
import torch
import pandas as pd
from datetime import datetime  # added for timestamped logging

# ==== Paths ====
EMB_DIR = Path("embeddings")
CHUNK_DIR = Path("chunks")
EMB_DF_PATH = EMB_DIR / "all_embeddings.pkl"
FAISS_PATH = EMB_DIR / "faiss_index.bin"

# ==== Query embedding model ====
tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")
model.eval()

# Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def embed_text(text: str):
    """Embed + normalize text for FAISS search."""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
    return embeddings.numpy().astype("float32")


def load_index_and_count():
    """Load FAISS index and return how many embeddings exist."""
    if not FAISS_PATH.exists() or not EMB_DF_PATH.exists():
        print("❌ Missing embeddings files.")
        return None, 0

    print("📌 Loading FAISS index + metadata...")
    index = faiss.read_index(str(FAISS_PATH))
    df = pd.read_pickle(EMB_DF_PATH)
    total = df.shape[0]

    print(f"✅ Loaded FAISS index + {total} chunk embeddings")
    return index, total


def retrieve_context(query, index, total_chunks, top_k=3):
    """Search for top_k similar chunks and return text contents."""
    print(f"[{datetime.utcnow().isoformat()}] retrieve_context ENTER: query_len={len(query) if query else 0}, top_k={top_k}, total_chunks={total_chunks}")

    if index is None:
        print(f"[{datetime.utcnow().isoformat()}] retrieve_context: index is None")
        return "No index available."

    # 1) Embed the query with error handling
    print('KAI 3: querying FAISS')
    try:
        query_vec = embed_text(query)
        print(f"[{datetime.utcnow().isoformat()}] embed_text returned type={type(query_vec)} shape={getattr(query_vec,'shape',None)} dtype={getattr(query_vec,'dtype',None)}")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] embed_text ERROR: {e}")
        raise
    print('KAI 4: querying FAISS done')

    # 2) Ensure query_vec is 2D float32 contiguous array expected by FAISS
    try:
        if isinstance(query_vec, np.ndarray):
            if query_vec.ndim == 1:
                query_vec = query_vec.reshape(1, -1)
            query_vec = np.ascontiguousarray(query_vec, dtype="float32")
        else:
            print(f"[{datetime.utcnow().isoformat()}] Warning: query_vec unexpected type {type(query_vec)} - attempting conversion")
            query_vec = np.ascontiguousarray(np.array(query_vec, dtype="float32").reshape(1, -1))
        print(f"[{datetime.utcnow().isoformat()}] query_vec normalized shape={query_vec.shape} dtype={query_vec.dtype} contiguous={query_vec.flags['C_CONTIGUOUS']}")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] query_vec normalization ERROR: {e}")
        raise

    # 3) Call FAISS index.search with error handling and debug prints
    try:
        print(f"[{datetime.utcnow().isoformat()}] Calling index.search(top_k={top_k})...")
        D, I = index.search(query_vec, top_k)
        print(f"[{datetime.utcnow().isoformat()}] index.search returned D.shape={getattr(D,'shape',None)} I.shape={getattr(I,'shape',None)}")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] index.search ERROR: {e}")
        raise

    # 4) Iterate results with detailed logs and robust checks
    context_blocks = []
    try:
        row = I[0] if (hasattr(I, "__len__") and len(I) > 0) else I
        for pos, raw_idx in enumerate(row):
            try:
                print(f"[{datetime.utcnow().isoformat()}] result[{pos}] raw_idx={raw_idx} type={type(raw_idx)}")
                if not isinstance(raw_idx, (int, np.integer)):
                    raw_idx = int(raw_idx)
                if raw_idx < 0 or raw_idx >= total_chunks:
                    print(f"[{datetime.utcnow().isoformat()}] Skipping out-of-range idx={raw_idx}")
                    continue
                chunk_path = CHUNK_DIR / f"{raw_idx}.txt"
                exists = chunk_path.exists()
                print(f"[{datetime.utcnow().isoformat()}] chunk_path={chunk_path} exists={exists}")
                if exists:
                    chunk_text = chunk_path.read_text()
                    context_blocks.append(f"📄 Chunk {raw_idx}\n{chunk_text}")
            except Exception as inner_e:
                print(f"[{datetime.utcnow().isoformat()}] Error processing result[{pos}]: {inner_e}")
                continue
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Error iterating search results: {e}")
        raise

    context = "\n\n---\n\n".join(context_blocks) if context_blocks else "No relevant retrieved chunks."
    print(f"[{datetime.utcnow().isoformat()}] Retrieved context (chars={len(context)}) blocks={len(context_blocks)}")
    return context


def chat(message, history, index, total_chunks):
    if index is None:
        print(f"[{datetime.utcnow().isoformat()}] Attempted chat but embeddings index missing.")
        return "⚠️ No embeddings available. Run embedding generation first."

    # log start of chat handling
    print(f"[{datetime.utcnow().isoformat()}] Starting chat handling for message: {message!r}")
    print('\t\t\tKAI1')

    context = retrieve_context(message, index, total_chunks)
    print('\t\t\tKAI2')

    prompt = f"""
You are a helpful assistant answering questions using the retrieved context.

Context:
{context}

User Question: {message}

If the context is not relevant, say so.
"""

    # Log that we'll call the Anthropic API
    print(f"[{datetime.utcnow().isoformat()}] Making Anthropic API call...")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        # Try to extract text similarly to existing code; fall back to string conversion
        try:
            resp_text = response.content[0].text
        except Exception:
            resp_text = str(response)

        # log response received (truncate to avoid overwhelming terminal)
        max_print = 2000
        print(f"[{datetime.utcnow().isoformat()}] Anthropic response received (chars={len(resp_text)}).")
        print(f"[{datetime.utcnow().isoformat()}] Response preview: {resp_text[:max_print]!s}")

        return resp_text
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Error calling Anthropic API: {e}")
        return "⚠️ Error communicating with Anthropic API. See server logs."


if __name__ == "__main__":
    index, total_chunks = load_index_and_count()
    if index is None:
        exit(1)

    print("✅ Ready! Launching Gradio UI...")

    with gr.Blocks(title="RAG Chatbot") as demo:
        gr.Markdown("# 📚 RAG Chatbot (Anthropic)")
        chatbot = gr.Chatbot(height=500)
        msg = gr.Textbox(label="Ask about your documents...")
        clear = gr.Button("Clear chat")

        def respond(message, chat_history):
            if not message.strip():
                return "", chat_history
            # print each user message entering the system
            print(f"[{datetime.utcnow().isoformat()}] User submitted message: {message!r}")
            bot_msg = chat(message, chat_history, index, total_chunks)
            chat_history.append((message, bot_msg))
            # print after getting the bot response
            print(f"[{datetime.utcnow().isoformat()}] Appended bot response to history. (response chars={len(bot_msg)})")
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: [], None, chatbot, queue=False)

    demo.launch()
    demo.launch(share=True)

