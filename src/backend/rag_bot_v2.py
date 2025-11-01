import os
import pickle
import numpy as np
from pathlib import Path
import gradio as gr
import faiss
from transformers import AutoTokenizer, AutoModel
import anthropic
import torch

# Init tokenizer + model for queries
tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")
model.eval()

# Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def embed_text(text):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
    return embeddings.numpy()[0]

def load_embeddings():
    embeddings_dir = Path("embeddings")
    if not embeddings_dir.exists():
        return None, None, None

    try:
        index = faiss.read_index(str(embeddings_dir / "faiss_index.bin"))
        with open(embeddings_dir / "documents.pkl", "rb") as f:
            documents = pickle.load(f)
        with open(embeddings_dir / "filenames.pkl", "rb") as f:
            filenames = pickle.load(f)
        print(f"Loaded {len(documents)} embedded documents.")
        return index, documents, filenames
    except Exception as e:
        print(f"Error loading embeddings: {e}")
        return None, None, None

def retrieve_context(query, index, documents, filenames, top_k=3):
    query_emb = embed_text(query)
    query_emb = np.array([query_emb]).astype('float32')
    distances, indices = index.search(query_emb, top_k)

    context_parts = []
    for idx in indices[0]:
        context_parts.append(f"Document: {filenames[idx]}\n{documents[idx]}")
    
    return "\n\n---\n\n".join(context_parts)

def chat(message, history, index, documents, filenames):
    if index is None:
        return "⚠️ No embeddings found. Run generate_embeddings.py first."

    context = retrieve_context(message, index, documents, filenames)

    prompt = f"""
You are a helpful assistant answering questions based on the provided documents.

Context:
{context}

Question: {message}

If the context doesn't contain relevant information, say so.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

if __name__ == "__main__":
    print("\nLoading FAISS index + docs...")
    index, documents, filenames = load_embeddings()

    if index is None:
        print("❌ No embeddings available. Run: python generate_embeddings.py")
        exit(1)

    print("✅ Ready! Launching Gradio...")

    with gr.Blocks(title="RAG Chatbot") as demo:
        gr.Markdown("# 📚 RAG Chatbot (Anthropic)")
        chatbot = gr.Chatbot(height=500)
        msg = gr.Textbox(label="Ask a question...")
        clear = gr.Button("Clear Chat")

        def respond(message, chat_history):
            if not message.strip():
                return "", chat_history
            bot_msg = chat(message, chat_history, index, documents, filenames)
            chat_history.append((message, bot_msg))
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: [], None, chatbot, queue=False)

    demo.launch()
