import gradio as gr
import base64

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
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
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
