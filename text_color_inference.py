import colorsys
import html
import gradio as gr

def score_to_hex_hsl(score: float, sat: float = 0.85, light: float = 0.40) -> str:
    """Convert a score (0–1) into a color between red and green."""
    s = max(0.0, min(1.0, float(score)))
    hue = (120.0 * s) / 360.0  # 0 (red) -> 120 (green)
    r, g, b = colorsys.hls_to_rgb(hue, light, sat)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def render_colored_text(score: float, text: str) -> str:
    color = score_to_hex_hsl(score)
    safe = html.escape(text).replace("\n", "<br>")
    return f"""
    <div style="font-family: system-ui, -apple-system, Segoe UI, Arial; font-size: 18px; line-height: 1.5;">
      <div style="margin-bottom: 8px;">
        <strong>Score:</strong> {score:.2f}
        &nbsp;&nbsp; <strong>Color:</strong> <code>{color}</code>
        <span style="display:inline-block; margin-left:10px; padding:4px 8px; border-radius:6px; color:#fff; background:{color};">
          Preview
        </span>
      </div>
      <div style="padding: 10px 0; color: {color};">
        {safe}
      </div>
    </div>
    """

with gr.Blocks(title="Text Color Inference (Gradio)") as demo:
    gr.Markdown("# Text Color Inference (Gradio)\nColor text by trust score from **red → green**.")
    with gr.Row():
        score = gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Trust score (0–1)")
    text = gr.Textbox(
        label="Chatbot response",
        value="This is the chatbot answer. Move the slider to change my color.",
        lines=6
    )
    out = gr.HTML(render_colored_text(0.5, "This is the chatbot answer. Move the slider to change my color."))

    score.change(render_colored_text, [score, text], out)
    text.change(render_colored_text, [score, text], out)

if __name__ == "__main__":
    demo.launch()
