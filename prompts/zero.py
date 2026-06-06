# Zero Shot Prompting 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


# Zero Shot Prompting: Directly giving the inst to LLM 
SYSTEM_PROMPT = "You should only and only ans the coding related questions. Do not answer anything else. Your name is CAASI. If user asks something other than coding, Just say sorry"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content" : "Hey, Can to write a python code to translate a english word to hindi"}
    ]
)

print(response.choices[0].message.content)