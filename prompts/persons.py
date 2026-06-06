# Zero Shot Prompting 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


# Zero Shot Prompting: Directly giving the inst to LLM 
SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Braj.
     You are acting on behalf of Braj who is 25 years old Tech enthusiatic and 
     senior software engineer. Your main tech stack is JS Python and you are learning GenAI these days.

     Examples:
     Q. Hey
     A: Hey, whats up!
"""


response = client.chat.completions.create(
    model="gpt-4o-mini",
    # response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content" : "Hey there"}
    ]
)

print(response.choices[0].message.content)