# ============================================
# File 2: chatbot.py
# Save this as chatbot.py (in the same directory as responses.py)

import gradio as gr
from fixed_text import (
    DYSLEXIA_RESPONSE,
    DYSLEXIA_KEYWORDS,
    DYSPRAXIA_RESPONSE,
    DYSPRAXIA_KEYWORDS,
    CHATBOT_TITLE,
    CHATBOT_DESCRIPTION,
    DEFAULT_RESPONSE,
)

keyword_response_map = {
    tuple(DYSLEXIA_KEYWORDS): DYSLEXIA_RESPONSE,
    tuple(DYSPRAXIA_KEYWORDS): DYSPRAXIA_RESPONSE,
}

def chatbot_response(message, history):
    """
    Returns a hardcoded response based on the user's message.
    
    Args:
        message: The user's input message
        history: The chat history (list of [user_message, bot_response] pairs)
    
    Returns:
        A hardcoded response string
    """
    message_lower = message.lower()
    
    # Map keyword groups to responses for cleaner, extensible logic

    for keywords, response in keyword_response_map.items():
        if any(keyword in message_lower for keyword in keywords):
            return response

    # Default response
    return DEFAULT_RESPONSE

# Create the Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chatbot_response,
    title=CHATBOT_TITLE,
    description=CHATBOT_DESCRIPTION,
    examples=[DYSLEXIA_KEYWORDS, DYSPRAXIA_KEYWORDS],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()