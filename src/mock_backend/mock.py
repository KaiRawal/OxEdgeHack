import numpy as np
import pandas as pd
from pathlib import Path
# ...existing code...
# from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel
import torch

EMB_DIR = Path("embeddings")
# ...existing code...

# ---------------------------------------------------------------------
# Configuration for ModernBERT
# ---------------------------------------------------------------------
DOCS_DIR = Path("docs")
CHUNKS_DIR = Path("chunks")
MODEL_NAME = "answerdotai/ModernBERT-base"
CHUNK_SIZE = 512
DEVICE = "cpu"

def load_model():
    print("📌 Loading ModernBERT model (CPU)...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    return tokenizer, model

# load once at module import (CPU)
_tokenizer, _bert_model = load_model()

def embed_text(text: str) -> np.ndarray:
    """
    Embed a short text using ModernBERT on CPU.
    Returns a 1-D float32 numpy array (L2-normalized).
    """
    tokens = _tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(DEVICE)
    with torch.no_grad():
        outputs = _bert_model(**tokens)
        pooled = outputs.last_hidden_state.mean(dim=1)  # (1, dim)
        pooled = pooled / pooled.norm(dim=1, keepdim=True)
    return pooled.cpu().numpy().astype("float32")[0]  # return 1-D array

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1-D numpy arrays. Returns float in [-1, 1]."""
    if a is None or b is None:
        return 0.0
    a = a.flatten().astype(np.float32)
    b = b.flatten().astype(np.float32)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def similarity(response):
    resp = response
    print('SIMILARITY FUNCTION OUTPUT:')
    print(resp)
    print(type(resp))
    # embedding_matrix = pd.read_pickle(EMB_DIR / "all_embeddings.pkl")
    # doc_embed = embedding_matrix.iloc[embed_ind].values[embed_ind]
    # Load two doc embeddings and take their mean
    docs_dir = Path("embeddings")
    doc0 = np.load(docs_dir / "nhsdoc2_0.npy")
    doc1 = np.load(docs_dir / "nhsdoc2_1.npy")
    doc_embed = ((doc0.astype('float32') + doc1.astype('float32')) / 2.0).astype('float32')

    print(doc_embed.shape)
    # iterate over items in resp (expecting iterable of (text, something))
    for text_item in resp:
        # embed the short text using ModernBERT helper (returns 1-D numpy array)
        resp_embed = embed_text(text_item)
        sim = cosine_sim(resp_embed, doc_embed)
        # store similarity back keyed by the original text
        resp[text_item] = sim

    return resp




# ============================================
# File 2: chatbot.py
# Save this as chatbot.py (in the same directory as responses.py)

import gradio as gr
import colorsys
import html
import base64
import os
from fixed_text import (
    DYSLEXIA_RESPONSE,
    DYSLEXIA_RESPONSES,
    DYSLEXIA_KEYWORDS,
    DYSPRAXIA_RESPONSE,
    DYSPRAXIA_RESPONSES,
    DYSPRAXIA_KEYWORDS,
    CHATBOT_TITLE,
    CHATBOT_DESCRIPTION,
    DEFAULT_RESPONSE,
)

keyword_response_map = {
    tuple(DYSLEXIA_KEYWORDS): DYSLEXIA_RESPONSES,
    tuple(DYSPRAXIA_KEYWORDS): DYSPRAXIA_RESPONSES,
}

def clamp01(x):
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0

def score_to_hex(score: float) -> str:
    """Convert [0,1] score to red→green hex colour (HSL hue 0→120)."""
    s = clamp01(score)
    hue = (120.0 * s) / 360.0
    r, g, b = colorsys.hls_to_rgb(hue, 0.40, 0.85)
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

def render_coloured_paragraphs(score_dict: dict, threshold: float = 0.0) -> str:
    """Render each paragraph with its colour based on score.
    If threshold > 0, hide paragraphs with score < threshold.
    """
    print(score_dict)
    # score_dict = similarity(score_dict)   
    # print(score_dict)
    thr = clamp01(threshold)
    blocks = []
    for para, score in score_dict.items():
        try:

            numeric_score = float(score)
        except Exception:
            numeric_score = 0.0
        if numeric_score < thr:
            continue  # skip low-score paragraphs
        colour = score_to_hex(numeric_score)
        safe_text = html.escape(str(para))
        blocks.append(
            f"<p style='color:{colour}; margin:0 0 12px 0;'>"
            f"{safe_text}"
            # f"<br><span style='opacity:0.85'>Trust: {clamp01(numeric_score):.2f} | Colour: {colour}</span>"
            f"</p>"
        )
    if not blocks:
        # no paragraphs passed the threshold
        return (
            "<div style='font-family:system-ui,Arial;line-height:1.6;font-size:17px;'>"
            f"<p style='color:#666;margin:0;'>No paragraphs with trust ≥ {thr:.2f}.</p>"
            "</div>"
        )
    return "<div style='font-family:system-ui,Arial;line-height:1.6;font-size:17px;'>" + "".join(blocks) + "</div>"

def format_response_obj(response, threshold: float = 0.0) -> str:
    """If response is a dict paragraph->score, render coloured HTML (respecting threshold); otherwise escape text."""
    print(response)
    print(type(response))
    if isinstance(response, dict):
        return render_coloured_paragraphs(response, threshold)
    # fallback: plain text (escaped)
    return f"<div style='font-family:system-ui,Arial;font-size:17px'>{html.escape(str(response))}</div>"

def get_response_for_message(message: str, threshold: float = 0.0) -> str:
    """
    Return HTML string for matched response (coloured if dict), otherwise default response.
    Threshold filters out low-score paragraphs when rendering.
    """
    message_lower = (message or "").lower()
    for keywords, response in keyword_response_map.items():
        if any(keyword in message_lower for keyword in keywords):
            return format_response_obj(response, threshold)
    return format_response_obj(DEFAULT_RESPONSE, threshold)

# Add global CSS and header helpers
def global_css():
    return """
    @import url('https://fonts.googleapis.com/css2?family=Istok+Web:wght@400;600&display=swap');

    /* NHS-like color variables */
    :root{
    --nhs-blue: #005EB8;      /* primary */
    --nhs-dark-blue: #003087; /* dark */
    --nhs-bright: #0072CE;    /* bright accent */
    --nhs-pale: #E8EDEE;      /* pale neutral background */
    --nhs-midgrey: #768692;   /* secondary text */
    --header-foreground: #ffffff;
    --card-bg: #ffffff;
    --page-bg: #F7FAFB;
    }
    /* Apply font app-wide (gradio container + body) */
    body, .gradio-container {
        font-family: 'Istok Web', Arial, sans-serif !important;
        background: var(--page-bg);
        color: #111111;
    }
    /* Page wrapper spacing */
    .gradio-container {
    padding: 18px !important;
    }
    /* Chat container card look */
    .gradio-container > .container {
    /* keep default - Blocks will wrap content - this is a gentle hint */
    }
    /* Style Gradio ChatInterface default elements as much as is safe */
    .gr-chatbot, .chatbot, .gradio-chatbot, .gradio-chatbot * {
    font-family: inherit;
    }
    /* Try to style chat bubbles (these selectors cover common Gradio class names;
    you may need to adjust depending on Gradio version) */
    .chatbot .user, .gr-chatbot .user, .chatbot .message.user {
    background: linear-gradient(180deg, rgba(0,94,184,0.95), rgba(0,94,184,0.95));
    color: #fff;
    border-radius: 14px;
    padding: 8px 12px;
    }
    /* bot bubble - light neutral */
    .chatbot .bot, .gr-chatbot .bot, .chatbot .message.bot {
    background: var(--nhs-pale);
    color: #101418;
    border-radius: 12px;
    padding: 8px 12px;
    }
    /* Make sure input textbox and send button use brand colours */
    .gr-textbox, textarea, input[type="text"] {
    font-family: inherit;
    border-radius: 8px;
    padding: 10px;
    border: 1px solid #d7dee3;
    background: #fff;
    }
    /* Primary buttons (send/examples) */
    .gr-button, button, .gradio-button {
    font-family: inherit;
    background: linear-gradient(180deg,var(--nhs-bright),var(--nhs-blue));
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 8px 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }
    /* Secondary / example style (outline) */
    .example-btn {
    background: transparent;
    color: var(--nhs-blue);
    border: 1px solid rgba(0,94,184,0.12);
    border-radius: 8px;
    padding: 8px 10px;
    }
    /* Links & interactive text */
    a, a:visited {
    color: var(--nhs-blue);
    }
    /* Small helpers: muted text */
    .small-muted {
    color: var(--nhs-midgrey);
    font-size: 0.9rem;
    }
    /* Ensure good contrast for accessibility */
    input, textarea, select {
    color: #111;
    }
    /* Responsive tweak */
    @media (max-width: 900px) {
    .gradio-container { padding: 12px !important; }
    }
    /* Fix contrast for refresh / clear / retry icons in ChatInterface footer */
    button svg, .gr-button svg {
    filter: brightness(0) invert(1) !important;  /* makes icons white */
    }
    .gr-button, button, .gradio-button {
    background: var(--nhs-blue) !important;
    color: #ffffff !important;
    }
    /* Optional: hover state for better feedback */
    .gr-button:hover, button:hover, .gradio-button:hover {
    background: var(--nhs-dark-blue) !important;
    }
    /* Hide Gradio footer */
    footer, .svelte-drumef, .gradio-container footer {
        display: none !important;
    }
    .svelte-phx28p {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    """

def encode_image_to_base64(image_path):
    # Try a few candidate paths (input path, relative to this file, resources folder)
    candidates = [
        image_path,
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", image_path)),
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "resources", os.path.basename(image_path))),
        os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "resources", os.path.basename(image_path))),
    ]
    for p in candidates:
        try:
            if os.path.exists(p):
                with open(p, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception:
            continue
    return ""  # fallback to empty string if image not found

# Attempt to load the logo using the provided path; safe if missing
LOGO_BASE64 = encode_image_to_base64("src/resources/NHS_logo.png")

def header():
    return gr.HTML(
        f"""
        <div style="
            background-color:#005EB8;
            padding:16px;
            padding-left: 0;
            padding-right: 0;
            margin-left: 0;
            margin-right: 0;
            border-radius:8px;
            display:flex;
            align-items:center;
            gap:15px;
            color:white;
        ">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="NHS Logo" style="height:50px;border-radius:6px;margin-left: 20px;">
            <h1 style="margin:0;font-size:1.6em;color:#ffffff; ">NHS Chatbot</h1>
        </div>
        """,
    )

# Replace ChatInterface with Blocks-based UI that shows coloured HTML output
with gr.Blocks(title=CHATBOT_TITLE) as demo:
    # inject global CSS
    gr.HTML(f"<style>{global_css()}</style>")
    # show header
    header()
    gr.HTML(f"<h3 style='margin-top:0;padding-top:0;padding-bottom:25px;'>{html.escape(CHATBOT_DESCRIPTION)}</h3>")
    inp = gr.Textbox(label="Message", placeholder="Type your message...")
    # new slider: default 0.0 (disabled), step 0.01
    threshold_slider = gr.Slider(0.0, 1.0, value=0.0, step=0.01, label="Trust threshold (hide paragraphs with score < value)")
    out = gr.HTML("<div >Responses will appear here.</div>")
    btn = gr.Button("Send")

    def on_submit(message, threshold):
        return get_response_for_message(message, threshold)

    btn.click(on_submit, [inp, threshold_slider], out)
    inp.submit(on_submit, [inp, threshold_slider], out)

if __name__ == "__main__":
    demo.launch(share=True)