# File 1: responses.py
# Save this as responses.py

"""
Configuration file containing all hardcoded chatbot responses.
"""

# Response mappings - keyword to response
GREETING_RESPONSE = "Hello! How can I help you today?"

HOW_ARE_YOU_RESPONSE = "I'm doing great! Thanks for asking. I'm a simple chatbot with hardcoded responses."

NAME_RESPONSE = "I'm a Simple Chatbot. I don't use any APIs - just hardcoded responses!"

GOODBYE_RESPONSE = "Goodbye! Have a great day!"

HELP_RESPONSE = "I'm a simple chatbot. Try saying 'hello', asking 'how are you', or say 'bye'!"

WEATHER_RESPONSE = "I don't have access to real weather data, but I hope it's nice where you are!"

THANK_YOU_RESPONSE = "You're welcome! Happy to help!"

DEFAULT_RESPONSE = "I'm a simple chatbot with limited responses. Try asking me something else!"

# Keywords for matching (lowercase)
GREETING_KEYWORDS = ["hello", "hi", "hey"]
HOW_ARE_YOU_KEYWORDS = ["how are you", "how're you"]
NAME_KEYWORDS = ["name", "who are you"]
GOODBYE_KEYWORDS = ["bye", "goodbye", "see you"]
HELP_KEYWORDS = ["help"]
WEATHER_KEYWORDS = ["weather"]
THANK_KEYWORDS = ["thank"]

# Example prompts for the UI
EXAMPLE_PROMPTS = [
    "Hello!",
    "How are you?",
    "What's your name?",
    "What's the weather like?",
    "Goodbye!"
]

# UI Configuration
CHATBOT_TITLE = "NHS Chatbot"
CHATBOT_DESCRIPTION = "Ask any health-related questions."


