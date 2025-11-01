# ============================================
# File 2: chatbot.py
# Save this as chatbot.py (in the same directory as responses.py)

import gradio as gr
import colorsys
import html
from mock_ui import global_css, header, favicon, description
from fixed_text import (
    DYSLEXIA_RESPONSE,
    DYSLEXIA_RESPONSES,
    DYSLEXIA_KEYWORDS,
    DYSPRAXIA_RESPONSE,
    DYSPRAXIA_KEYWORDS,
    CHATBOT_TITLE,
    CHATBOT_DESCRIPTION,
    DEFAULT_RESPONSE,
)

keyword_response_map = {
    tuple(DYSLEXIA_KEYWORDS): DYSLEXIA_RESPONSES,
    tuple(DYSPRAXIA_KEYWORDS): DYSPRAXIA_RESPONSE,
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

# Replace ChatInterface with Blocks-based UI that shows coloured HTML output
with gr.Blocks(
    title=CHATBOT_TITLE,
    theme=gr.themes.Soft(),
    css=global_css()
) as demo:

    header()
    favicon()

    description(CHATBOT_DESCRIPTION)

    inp = gr.Textbox(label="Message", placeholder="Ask me any health-related questions...")
    out = gr.HTML("<div>Responses will appear here.</div>")
    btn = gr.Button("Send")

    def on_submit(message):
        return get_response_for_message(message)

    btn.click(on_submit, inp, out)
    inp.submit(on_submit, inp, out)

if __name__ == "__main__":
    demo.launch()