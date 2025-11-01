# ============================================
# File 2: chatbot.py
# Save this as chatbot.py (in the same directory as responses.py)

import gradio as gr
from fixed_text import (
    GREETING_RESPONSE,
    HOW_ARE_YOU_RESPONSE,
    NAME_RESPONSE,
    GOODBYE_RESPONSE,
    HELP_RESPONSE,
    WEATHER_RESPONSE,
    THANK_YOU_RESPONSE,
    DEFAULT_RESPONSE,
    GREETING_KEYWORDS,
    HOW_ARE_YOU_KEYWORDS,
    NAME_KEYWORDS,
    GOODBYE_KEYWORDS,
    HELP_KEYWORDS,
    WEATHER_KEYWORDS,
    THANK_KEYWORDS,
    EXAMPLE_PROMPTS,
    CHATBOT_TITLE,
    CHATBOT_DESCRIPTION
)

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
    
    # Check for greeting
    if any(keyword in message_lower for keyword in GREETING_KEYWORDS):
        return GREETING_RESPONSE
    
    # Check for "how are you"
    elif any(keyword in message_lower for keyword in HOW_ARE_YOU_KEYWORDS):
        return HOW_ARE_YOU_RESPONSE
    
    # Check for name question
    elif any(keyword in message_lower for keyword in NAME_KEYWORDS):
        return NAME_RESPONSE
    
    # Check for goodbye
    elif any(keyword in message_lower for keyword in GOODBYE_KEYWORDS):
        return GOODBYE_RESPONSE
    
    # Check for help
    elif any(keyword in message_lower for keyword in HELP_KEYWORDS):
        return HELP_RESPONSE
    
    # Check for weather
    elif any(keyword in message_lower for keyword in WEATHER_KEYWORDS):
        return WEATHER_RESPONSE
    
    # Check for thank you
    elif any(keyword in message_lower for keyword in THANK_KEYWORDS):
        return THANK_YOU_RESPONSE
    
    # Default response
    else:
        return DEFAULT_RESPONSE

# Create the Gradio ChatInterface
demo = gr.ChatInterface(
    fn=chatbot_response,
    title=CHATBOT_TITLE,
    description=CHATBOT_DESCRIPTION,
    examples=EXAMPLE_PROMPTS,
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()