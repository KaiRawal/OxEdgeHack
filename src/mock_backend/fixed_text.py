# File 1: responses.py
# Save this as responses.py

"""
Configuration file containing all hardcoded chatbot responses.
"""



# Response mappings - keyword to response

DYSLEXIA_RESPONSES = {"<pulling in NHS dyslexia data> Here are some common Signs of Dyslexia:": 0.1,
"1. Reading and Writing Difficulties": 0.1,
"2. Reading and writing very slowly": 0.3,
"3. Confusing the order of letters in words": 0.1,
"4. Getting confused by letters that look similar and writing letters the wrong way round (such as 'b' and 'd')": 0.1,
"5. Poor or inconsistent spelling": 0.5,
"6. Processing and Organization:": 0.7,
"7. Finding it hard to carry out a sequence of directions": 0.9,
"8. Struggling with planning and organization": 0.1,
"9. Understanding information when told verbally, but having difficulty with information that's written down": 0.1,
"Do your symptoms match these?": 0.1,
}


DYSLEXIA_RESPONSE = """<pulling in NHS dyslexia data> Here are some common Signs of Dyslexia:
1. Reading and Writing Difficulties
2. Reading and writing very slowly
3. Confusing the order of letters in words
4. Getting confused by letters that look similar and writing letters the wrong way round (such as "b" and "d")
5. Poor or inconsistent spelling
6. Processing and Organization:
7. Finding it hard to carry out a sequence of directions
8. Struggling with planning and organization
9. Understanding information when told verbally, but having difficulty with information that's written down

Do your symptoms match these?
"""

DYSPRAXIA_RESPONSES = {
    "<pulling in NHS dyslexia data> Based on NHS information, here are the symptoms of dyspraxia (also known as Developmental Co-ordination Disorder or DCD) in children" : 0.9,
"1. Problems with movement and coordination are the main symptoms NHS, including:": 0.5,
"""Physical Activities:
- Difficulty with playground activities such as hopping, jumping, running, and catching or kicking a ball NHS
- Appearing awkward and clumsy - they may bump into objects, drop things and fall over a lot NHS
""": 0.4,
"""
2. Fine Motor Skills:
- Problems with writing, drawing and using scissors – their handwriting and drawings may appear scribbled and less developed compared to other children their age NHS
- Difficulty getting dressed, doing up buttons and tying shoelaces NHS
""": 0.3,
"""
3. Movement:
- Difficulty keeping still – they may swing or move their arms and legs a lot NHS
- Early Developmental Signs
- Early developmental milestones of crawling, walking, self-feeding and dressing may be delayed in young children with DCD. Drawing, writing and performance in sports are also usually behind what is expected for their age NHS.
""": 0.2,
"""
4. Other Associated Issues
- Some children with DCD have difficulty coordinating the movements required to produce clear speech NHS
- Behaviour problems – often stemming from a child's frustration with their symptoms NHS
""": 0.1,
"""
In Adults, symptoms of dyspraxia can vary between individuals and may change over time. You may find routine tasks difficult.
When to Seek Help: See a GP if you think you may have undiagnosed dyspraxia or problems with your coordination. It's a good idea to keep a diary of your symptoms."
""": 0.1,
}

DYSPRAXIA_RESPONSE = """<pulling in NHS dyslexia data> Based on NHS information, here are the symptoms of dyspraxia (also known as Developmental Co-ordination Disorder or DCD) in children
1. Problems with movement and coordination are the main symptoms NHS, including:
Physical Activities:
- Difficulty with playground activities such as hopping, jumping, running, and catching or kicking a ball NHS
- Appearing awkward and clumsy - they may bump into objects, drop things and fall over a lot NHS
2. Fine Motor Skills:
- Problems with writing, drawing and using scissors – their handwriting and drawings may appear scribbled and less developed compared to other children their age NHS
- Difficulty getting dressed, doing up buttons and tying shoelaces NHS
3. Movement:
- Difficulty keeping still – they may swing or move their arms and legs a lot NHS
- Early Developmental Signs
- Early developmental milestones of crawling, walking, self-feeding and dressing may be delayed in young children with DCD. Drawing, writing and performance in sports are also usually behind what is expected for their age NHS.
4. Other Associated Issues
- Some children with DCD have difficulty coordinating the movements required to produce clear speech NHS
- Behaviour problems – often stemming from a child's frustration with their symptoms NHS

In Adults, symptoms of dyspraxia can vary between individuals and may change over time. You may find routine tasks difficult.
When to Seek Help: See a GP if you think you may have undiagnosed dyspraxia or problems with your coordination. It's a good idea to keep a diary of your symptoms."""



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

