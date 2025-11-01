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


TRIGGER_RESPONSE = "Based on the NHS information, here's what can trigger depression:
Life-Changing Events
Sometimes there's a trigger for depression. Life-changing events can bring it on, such as:

Bereavement
Losing your job
Giving birth

Family History
People with a family history of depression are more likely to experience it themselves.
No Obvious Reason
You can also become depressed for no obvious reason - sometimes depression occurs without any clear trigger.
Important Distinction
It's worth noting that most people experience feelings of stress, anxiety or low mood during difficult times. A low mood may improve after a short period of time, rather than being a sign of depression. Depression is characterized by feeling persistently sad for weeks or months, rather than just a few days.
When to Seek Help
It's important to seek help from a GP if you think you may be depressed. Many people wait a long time before seeking help for depression, but it's best not to delay. The sooner you see a doctor, the sooner you can be on the way to recovery.
With the right treatment and support, most people with depression can make a full recovery.RetryShow does depression present in childrenI don't have specific information about how depression presents in children in the NHS documents provided to me. The documents I have focus on depression in adults, and they mention there is separate information about depression in children and young people, but those details aren't included in what I have access to.
If you'd like to know about the signs and symptoms of depression in children, I can search for current NHS information on this topic for you. Would you like me to do that?
Alternatively, I can provide you with information about the conditions that are covered for children in the documents I have - such as ADHD in children, autism in children, or dyslexia."

CHILDREN_RESPONSE = "Key Signs and Symptoms
Emotional Symptoms:

Prolonged feelings of sadness or hopelessness NHS
Irritability NHS 111 Wales
Excessive feelings of guilt and low self-esteem NHS 111 Wales

Behavioral Changes:

Loss of interest in activities, friends or family NHS 111 Wales
Inability to concentrate NHS 111 Wales
Problem behaviour can be a sign of depression in children and young people NHS
Withdrawal from home or school NHS

Physical Symptoms:

Physical symptoms, such as headaches and stomach aches NHS
A marked change in appetite NHS 111 Wales
Sleeping too little at night or too much during the day NHS 111 Wales
Disturbances in sleep patterns and tiredness NHS

School-Related Issues:

Problems at school can be a sign of depression NHS

Important Differences from Adults
Depression may even masquerade as bad behaviour, particularly in boys Wikipedia, and mood is characteristically much more variable and less pervasive than in adults, and rapid mood swings often occur Wikipedia.
Co-occurring Issues
Some children have problems with anxiety as well as depression NHS, and older children who are depressed may misuse drugs or alcohol.
When to Seek Help
If you think your child may be depressed, or you're concerned about their general wellbeing, make an appointment with them to see a GP NHS. The GP can refer your child to specialist children and young people's mental health services if necessary."



# Keywords for matching (lowercase)
DYSLEXIA_KEYWORDS = ["dyslexia"]
DYSPRAXIA_KEYWORDS = ["dyspraxia"]
TRIGGER_KEYWORDS = ["trigger"]
CHILDREN_KEYWORDS = ["children"]

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

