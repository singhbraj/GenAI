from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content": "You are an expert in Maths and only and only ans maths related questions. That is query is not related to maths. Just say sorry and do not ans that "},
        {"role":"user", "content" : "Hey, can you help me to solve the a+b whole sqaure"}
    ]
)

print(response.choices[0].message.content)