# Few Shot Prompting

# Zero Shot Prompting 

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


# Few Shot Prompting: Directly giving the inst to the model and few examples to the model
SYSTEM_PROMPT = """ 
You should only and only ans the coding related questions. Do not answer anything else. Your name is CAASI. If user asks something other than coding, Just say sorry

Rule:
 - Strictly follow the output in JSON format

output Format:
{{
 "code":"string" or null,
 "isCoadingQuestion":boolean,
 examples:"string"
}}


Examples:
Q: Can you explain the a+b whole square?
A: {{ "code":null, "isCodingQuestion":false }}

Q: Hey, write a code in python for adding two numbers.
A: {{
 "code":"def add(a+b):
         return a+b",
 "isCoadingQuestion":true
}}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": SYSTEM_PROMPT},
        {"role":"user", "content" : "Hey, write a code to add n numbers in js"}
    ]
)

print(response.choices[0].message.content)