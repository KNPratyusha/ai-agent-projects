from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

messages = [
    {"role": "system", "content": """You are Aria, a sharp AI engineering mentor. 
You remember everything the user tells you.
You give concise, practical answers.
You occasionally encourage the user when they make progress."""}
]

print("Aria: Hi! I'm Aria. Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    
    if "quit" in user_input.lower():
        print("Aria: Goodbye!")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    
    print(f"Aria: {reply}")
    print(f"(memory: {len(messages)} messages)\n")
    