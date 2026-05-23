from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FRONTIER_MODEL = "llama-3.3-70b-versatile"

def generate_response(user_input, history=[]):
    messages = [{"role": "system", "content": "You are a helpful frontier AI assistant."}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model=FRONTIER_MODEL,
        messages=messages,
        max_tokens=512
    )
    return response.choices[0].message.content