from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

job_description = """
We are hiring an AI Engineer. Required skills:
Python, LLMs, Prompt Engineering, APIs, Vector Databases, LangChain, Docker
"""

candidate_skills = """
Pratyusha knows: Python, Prompt Engineering, APIs, LLMs, JSON
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": """You are a technical recruiter.
Analyze the candidate's skills against the job description.
Think step by step before scoring.
Then return ONLY this JSON, nothing else:
{
    "match_score": 0-100,
    "matching_skills": [],
    "missing_skills": [],
    "recommendation": ""
}"""},
        {"role": "user", "content": f"Job:\n{job_description}\n\nCandidate:\n{candidate_skills}"}
    ]
)

raw = response.choices[0].message.content
data = json.loads(raw)
print("\n--- CV Analysis Report ---")
print(f"Match Score:      {data['match_score']}%")
print(f"Matching Skills:  {', '.join(data['matching_skills'])}")
print(f"Missing Skills:   {', '.join(data['missing_skills'])}")
print(f"Recommendation:   {data['recommendation']}")
