from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def calculate(expression):
    try:
        result = eval(expression)
        return {"result": result}
    except:
        return {"error": "Invalid expression"}

def get_weather(city):
    weather_data = {
        "Hyderabad": {"temp": 34, "condition": "Sunny"},
        "Mumbai":    {"temp": 29, "condition": "Humid"},
        "Delhi":     {"temp": 38, "condition": "Hot"},
    }
    return weather_data.get(city, {"temp": "unknown", "condition": "unknown"})

def search_web(query):
    return {"result": f"Top result for '{query}': Simulated search result about {query}."}

def run_agent(user_message):
    print(f"\nUser: {user_message}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": """You are an agent with 3 tools.
Decide which tool to use and respond ONLY with JSON like this:
{"tool": "calculate", "input": "1234 * 5678"}
{"tool": "get_weather", "input": "Hyderabad"}
{"tool": "search_web", "input": "AI trends"}
{"tool": "none", "input": "your normal reply here"}
Nothing else. Only JSON."""},
            {"role": "user", "content": user_message}
        ]
    )

    raw = response.choices[0].message.content
    decision = json.loads(raw)
    tool = decision["tool"]
    inp = decision["input"]

    if tool == "calculate":
        result = calculate(inp)
        final_reply = f"The answer is {result['result']}"
    elif tool == "get_weather":
        result = get_weather(inp)
        final_reply = f"Weather in {inp}: {result['condition']}, {result['temp']}°C"
    elif tool == "search_web":
        result = search_web(inp)
        final_reply = result["result"]
    else:
        final_reply = inp

    print(f"Agent: {final_reply}")

run_agent("What is 1234 times 5678?")
run_agent("What's the weather in Hyderabad?")
run_agent("Search for latest trends in AI engineering")
run_agent("What is your name?")
