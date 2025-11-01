import gradio as gr
import colorsys
import html
import json
import ast

def clamp01(x):
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0

def score_to_hex(score: float) -> str:
    """Convert [0,1] score to red→green hex colour (HSL hue 0→120)."""
    s = clamp01(score)
    hue = (120.0 * s) / 360.0
    # colorsys.hls_to_rgb takes H,L,S in 0..1; we want fairly readable text
    r, g, b = colorsys.hls_to_rgb(hue, 0.40, 0.85)  # light=0.40, sat=0.85
    return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

def render_coloured_paragraphs(score_dict: dict) -> str:
    """Render each paragraph with its colour based on score."""
    blocks = []
    for para, score in score_dict.items():  # preserves insertion order
        colour = score_to_hex(score)
        safe_text = html.escape(str(para))
        blocks.append(
            f"<p style='color:{colour}; margin:0 0 12px 0;'>"
            f"{safe_text}"
            f"<br><span style='opacity:0.85'>Trust: {clamp01(score):.2f} | Colour: {colour}</span>"
            f"</p>"
        )
    return "<div style='font-family:system-ui,Arial;line-height:1.6;font-size:17px;'>" + "".join(blocks) + "</div>"

def parse_and_colour(text: str) -> str:
    """Accept Python dicts first, then JSON as fallback."""
    text = text.strip()
    if not text:
        return "<p>Paste a Python dict or JSON object mapping paragraph → score.</p>"

    # Try Python dict (single quotes etc.)
    try:
        data = ast.literal_eval(text)
        if not isinstance(data, dict):
            return "<p style='color:red'>Input must be a dict/object: {'Paragraph 1': 0.5, ...}</p>"
        return render_coloured_paragraphs(data)
    except Exception:
        pass

    # Fallback: JSON
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            return "<p style='color:red'>JSON must be an object: {\"Paragraph 1\": 0.5, ...}</p>"
        return render_coloured_paragraphs(data)
    except Exception as e2:
        return f"<p style='color:red'>Invalid input. Please provide a Python dict or JSON object.<br>Error: {html.escape(str(e2))}</p>"

example_py_dict = {
    'Paragraph 1: The model summarises the report.': 0.5,
    'Paragraph 2: The statement contains uncertain data.': 0.1,
    'Paragraph 3: The conclusion aligns with evidence.': 0.9
}

with gr.Blocks(title="Multi-Paragraph Trust Colouring") as demo:
    gr.Markdown("### 🧩 Multi-Paragraph Trust Visualiser\n"
                "Paste a **Python dict** (single quotes OK) or **JSON object** mapping paragraph → score (0..1).")
    inp = gr.Textbox(label="Input (Python dict or JSON)", value=str(example_py_dict), lines=10)
    out = gr.HTML(render_coloured_paragraphs(example_py_dict))
    btn = gr.Button("Render")
    btn.click(parse_and_colour, inp, out)
    inp.submit(parse_and_colour, inp, out)

if __name__ == "__main__":
    demo.launch()
