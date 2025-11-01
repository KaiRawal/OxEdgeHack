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

def render_coloured_paragraphs(score_dict: dict) -> str:
    """Render each paragraph with its colour based on score."""
    blocks = []
    for para, score in score_dict.items():
        colour = score_to_hex(score)
        safe_text = html.escape(str(para))
        blocks.append(
            f"<p style='color:{colour}; margin:0 0 12px 0;'>"
            f"{safe_text}"
            f"<br><span style='opacity:0.85'>Trust: {clamp01(score):.2f} | Colour: {colour}</span>"
            f"</p>"
        )
    return "<div style='font-family:system-ui,Arial;line-height:1.6;font-size:17px;'>" + "".join(blocks) + "</div>"

def format_response_obj(response) -> str:
    """If response is a dict paragraph->score, render coloured HTML; otherwise escape text."""
    print(response)
    print(type(response))
    if isinstance(response, dict):
        return render_coloured_paragraphs(response)
    # fallback: plain text (escaped)
    return f"<div style='font-family:system-ui,Arial;font-size:17px'>{html.escape(str(response))}</div>"

def get_response_for_message(message: str) -> str:
    """
    Return HTML string for matched response (coloured if dict), otherwise default response.
    """
    message_lower = (message or "").lower()
    for keywords, response in keyword_response_map.items():
        if any(keyword in message_lower for keyword in keywords):
            return format_response_obj(response)
    return format_response_obj(DEFAULT_RESPONSE)

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
            border-radius:8px;
            display:flex;
            align-items:center;
            gap:15px;
            color:white;
        ">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="NHS Logo" style="height:50px;border-radius:6px;">
            <h1 style="margin:0;font-size:1.6em;color:#ffffff;">NHS Chatbot</h1>
        </div>
        """,
    )

# Replace ChatInterface with Blocks-based UI that shows coloured HTML output
with gr.Blocks(title=CHATBOT_TITLE) as demo:
    # inject global CSS
    gr.HTML(f"<style>{global_css()}</style>")
    # show header
    header()
    gr.Markdown(f"### {CHATBOT_TITLE}\n\n{CHATBOT_DESCRIPTION}")
    inp = gr.Textbox(label="Message", placeholder="Type your message...")
    out = gr.HTML("<div >Responses will appear here.</div>")
    btn = gr.Button("Send")

    def on_submit(message):
        return get_response_for_message(message)

    btn.click(on_submit, inp, out)
    inp.submit(on_submit, inp, out)

if __name__ == "__main__":
    demo.launch()