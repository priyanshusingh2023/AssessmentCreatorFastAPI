API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`"
API_KEY = "AIzaSyCYutjs2BzQThKnA2q1hDNbZro4Al7N0Dw"
GENERATION_CONFIG = {
    "temperature": 1.0,
    "topK": 1,
    "topP": 1,
    "maxOutputTokens": 2048,
    "stopSequences": []
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
