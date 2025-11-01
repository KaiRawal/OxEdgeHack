import os
import pickle
import numpy as np
from pathlib import Path
import gradio as gr
import faiss
from transformers import AutoTokenizer, AutoModel
import torch
import anthropic

# Initialize models
print("Loading embedding model...")
tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
model = AutoModel.from_pretrained("answerdotai/ModernBERT-base")
model.eval()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def embed_text(text):
    """Generate embeddings for text using ModernBERT"""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        outputs = model(**inputs)
        # Use mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        # Normalize
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
    return embeddings.numpy()[0]

def create_embeddings():
    """Create embeddings for all documents in /docs directory"""
    docs_dir = Path("docs")
    embeddings_dir = Path("embeddings")
    embeddings_dir.mkdir(exist_ok=True)
    
    if not docs_dir.exists():
        print("Error: /docs directory not found!")
        return None, None, None
    
    documents = []
    embeddings = []
    filenames = []
    
    # Read all text files
    for file_path in docs_dir.glob("*.txt"):
        print(f"Processing {file_path.name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            filenames.append(file_path.name)
            
            # Generate embedding
            emb = embed_text(content)
            embeddings.append(emb)
    
    if not documents:
        print("No .txt files found in /docs directory!")
        return None, None, None
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings).astype('float32')
    
    # Create FAISS index
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity with normalized vectors)
    index.add(embeddings_array)
    
    # Save everything
    faiss.write_index(index, str(embeddings_dir / "faiss_index.bin"))
    with open(embeddings_dir / "documents.pkl", 'wb') as f:
        pickle.dump(documents, f)
    with open(embeddings_dir / "filenames.pkl", 'wb') as f:
        pickle.dump(filenames, f)
    
    print(f"Created embeddings for {len(documents)} documents")
    return index, documents, filenames

def load_embeddings():
    """Load existing embeddings"""
    embeddings_dir = Path("embeddings")
    
    if not embeddings_dir.exists():
        return None, None, None
    
    try:
        index = faiss.read_index(str(embeddings_dir / "faiss_index.bin"))
        with open(embeddings_dir / "documents.pkl", 'rb') as f:
            documents = pickle.load(f)
        with open(embeddings_dir / "filenames.pkl", 'rb') as f:
            filenames = pickle.load(f)
        print(f"Loaded {len(documents)} documents from embeddings")
        return index, documents, filenames
    except:
        return None, None, None

def retrieve_context(query, index, documents, filenames, top_k=3):
    """Retrieve most relevant documents for a query"""
    query_embedding = embed_text(query)
    query_embedding = np.array([query_embedding]).astype('float32')
    
    # Search
    distances, indices = index.search(query_embedding, top_k)
    
    # Build context
    context_parts = []
    for i, idx in enumerate(indices[0]):
        context_parts.append(f"Document: {filenames[idx]}\n{documents[idx]}")
    
    return "\n\n---\n\n".join(context_parts)

def chat(message, history, index, documents, filenames):
    """Handle chat interaction"""
    if index is None:
        return "Error: No embeddings loaded. Please ensure documents are in /docs directory and restart."
    
    # Retrieve relevant context
    context = retrieve_context(message, index, documents, filenames)
    
    # Create prompt for Claude
    prompt = f"""You are a helpful assistant answering questions based on the provided documents.

Context from documents:
{context}

Question: {message}

Please answer the question based on the context provided. If the context doesn't contain relevant information, say so."""
    
    # Get response from Claude
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

if __name__ == "__main__":
    # Initialize or load embeddings
    print("\n" + "="*50)
    index, documents, filenames = load_embeddings()

    if index is None:
        print("No existing embeddings found. Creating new embeddings...")
        index, documents, filenames = create_embeddings()
        
        if index is None:
            print("\nERROR: Failed to create embeddings!")
            print("Please ensure:")
            print("1. The /docs directory exists")
            print("2. There are .txt files in /docs directory")
            print("\nExiting...")
            exit(1)

    print("="*50 + "\n")
    print(f"✓ Successfully loaded {len(documents)} documents")
    print("Starting Gradio interface...\n")

    # Create Gradio interface
    with gr.Blocks(title="RAG Chatbot") as demo:
        gr.Markdown("# 📚 RAG Chatbot")
        gr.Markdown("Ask questions about your documents. The chatbot will retrieve relevant context and answer using Claude.")
        
        chatbot = gr.Chatbot(height=500)
        msg = gr.Textbox(label="Your Question", placeholder="Ask a question about your documents...")
        clear = gr.Button("Clear")
        
        def respond(message, chat_history):
            if not message.strip():
                return "", chat_history
            
            bot_message = chat(message, chat_history, index, documents, filenames)
            chat_history.append((message, bot_message))
            return "", chat_history
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch()