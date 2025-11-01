# File 1: responses.py
# Save this as responses.py

"""
Configuration file containing all hardcoded chatbot responses.
"""

# Response mappings - keyword to response
DYSLEXIA_RESPONSE = """Common Signs of Dyslexia:
Reading and Writing Difficulties
Reading and writing very slowly
Confusing the order of letters in words
Getting confused by letters that look similar and writing letters the wrong way round (such as "b" and "d")
Poor or inconsistent spelling
Processing and Organization:
Finding it hard to carry out a sequence of directions
Struggling with planning and organization
Understanding information when told verbally, but having difficulty with information that's written down
"""

DYSPRAXIA_RESPONSE = """Based on NHS information, here are the symptoms of dyspraxia (also known as Developmental Co-ordination Disorder or DCD):
Main Symptoms in Children
Problems with movement and coordination are the main symptoms NHS, including:
Physical Activities:
Difficulty with playground activities such as hopping, jumping, running, and catching or kicking a ball NHS
Appearing awkward and clumsy - they may bump into objects, drop things and fall over a lot NHS
Fine Motor Skills:
Problems with writing, drawing and using scissors – their handwriting and drawings may appear scribbled and less developed compared to other children their age NHS
Difficulty getting dressed, doing up buttons and tying shoelaces NHS
Movement:
Difficulty keeping still – they may swing or move their arms and legs a lot NHS
Early Developmental Signs
Early developmental milestones of crawling, walking, self-feeding and dressing may be delayed in young children with DCD. Drawing, writing and performance in sports are also usually behind what is expected for their age NHS.
Other Associated Issues
Some children with DCD have difficulty coordinating the movements required to produce clear speech NHS
Behaviour problems – often stemming from a child's frustration with their symptoms NHS
In Adults
Symptoms of dyspraxia can vary between individuals and may change over time. You may find routine tasks difficult NHS.
When to Seek Help
See a GP if you think you may have undiagnosed dyspraxia or problems with your coordination. It's a good idea to keep a diary of your symptoms NHS."""



# Keywords for matching (lowercase)
DYSLEXIA_KEYWORDS = ["dyslexia"]
DYSPRAXIA_KEYWORDS = ["dyspraxia"]

DEFAULT_RESPONSE = "I'm a simple chatbot with limited responses. Try asking me something else!"



# Example prompts for the UI
EXAMPLE_PROMPTS = [
    "I think I have Dyslexia! What are the symptoms?",
    "I think I have Dyspraxia! What are the symptoms?",
]

# UI Configuration

# UI Configuration
CHATBOT_TITLE = "NHS Chatbot"
CHATBOT_DESCRIPTION = "ChatGPT does not understand healthcare well. Talk to me instead!"

