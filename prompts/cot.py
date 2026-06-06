# Chain of Thought Prompting

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You are an expert AI Assistant in resolving user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 

    Rules: 
    - Strictly Follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input),
    PLAN (That can be multiple times) and finally OUTPUT (Which is going to the displayed to the user).

    Output JSON Format:
    {{"step":"START" | "PLAN" | "OUTPUT", "content":"string"}} 

    Example: 
     START: Hey, can you solve 2+3*5 / 10
     PLAN:{"step":"PLAN", "CONTENT:"Seems  like user is interested in math problem"}
     PLAN:{"step":"PLAN", "CONTENT:"looking at the problem, we should solve this using BODMAS method"}
     PLAN:{"step":"PLAN", "CONTENT:"Yes, The BODMAS is correct thing to be done here"}
     PLAN:{"step":"PLAN", "CONTENT:"first we must multiply 3*5=15"}
     PLAN:{"step":"PLAN", "CONTENT:"Now the new equation is 2+15 / 10 "}
     PLAN:{"step":"PLAN", "CONTENT:"We must perfrom divide that 15/10=1.5"}
     PLAN:{"step":"PLAN", "CONTENT:"Now the new equation is 2+1.5 = 3.5"}
     PLAN:{"step":"PLAN", "CONTENT:"Now finally lets perform the addition "}
     PLAN:{"step":"PLAN", "CONTENT:"Great, we have solved and finally left with 3.5 as answer"}
     PLAN:{"step":"OUTPUT", "CONTENT:"3.5"}
   

 """


print("\n\n\n")

message_history = [

        {"role":"system", "content": SYSTEM_PROMPT},


]


user_query = input("👈")
message_history.append({"role":"user", "content":user_query})

while True:
    response = client.chat.completions.create(
            model="gpt-4o-mini", 
            response_format={"type":"json_object"},
            messages=message_history
    )

    raw_result = (response.choices[0].message.content)
    message_history.append({"role":"assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break


# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     response_format={"type":"json_object"},
#     messages=[
#         {"role":"system", "content": SYSTEM_PROMPT},
#         {"role":"user", "content" : "Hey, write a code to add n numbers in js"},
#         {"role":"assistant", "content":json.dumps(
#             {"step":"PLAN", "content":"User wants a code snippet for adding n numbers in JavaScript."}
#         )}
#     ]
# )

# print(response.choices[0].message.content)

print("\n\n\n")