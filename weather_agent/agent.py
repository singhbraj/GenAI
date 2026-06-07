# Chain of Thought Prompting

from dotenv import load_dotenv
from openai import OpenAI
import requests

import json

load_dotenv()

client = OpenAI()


def get_weather(city:str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "SOmething went wrong"


available_tools ={
    "get_weather":get_weather
}


SYSTEM_PROMPT = """
    You are an expert AI Assistant in resolving user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The plan can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT. 
    You can also call a tool if required from the list of available tools.
    For every tool call wait for the observe step which is the output from from the called tool.

    Rules: 
    - Strictly Follow the given JSON output format.
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input),
    PLAN (That can be multiple times) and finally OUTPUT (Which is going to the displayed to the user).

    Output JSON Format:
    {{"step":"START" | "PLAN" | "OUTPUT" | "TOOL, "content":"string", "tool": string, "input":string}} 

    Available Tools:
    - get_weather(city:str): Takes city name as an input string and retuens the weather info about the city.


    Example 1: 
     START: Hey, can you solve 2+3*5 / 10
     PLAN:{"step":"PLAN", "content": "Seems  like user is interested in math problem"}
     PLAN:{"step":"PLAN", "content": "looking at the problem, we should solve this using BODMAS method"}
     PLAN:{"step":"PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
     PLAN:{"step":"PLAN", "content": "first we must multiply 3*5=15"}
     PLAN:{"step":"PLAN", "content": "Now the new equation is 2+15 / 10 "}
     PLAN:{"step":"PLAN", "content": "We must perfrom divide that 15/10=1.5"}
     PLAN:{"step":"PLAN", "content": "Now the new equation is 2+1.5 = 3.5"}
     PLAN:{"step":"PLAN", "content": "Now finally lets perform the addition "}
     PLAN:{"step":"PLAN", "content": "Great, we have solved and finally left with 3.5 as answer"}
     PLAN:{"step":"OUTPUT", "content": "3.5"}


    Example 2: 
     START: What is the weather if Delhi?
     PLAN:{"step":"PLAN", "content": "Seems  like user is interested getting weather of Delhi in India"}
     PLAN:{"step":"PLAN", "content": "Lets see if we have any available tool from the list of available tools"}
     PLAN:{"step":"PLAN", "content": "Great, we have get_weather tool available for this query."}
     PLAN:{"step":"PLAN", "content":  "I need to call get_weather tool for delhi as input for city"}
     PLAN:{"step":"TOOL", "tool": "get_weather", "input": "delhi"},
     PLAN:{"step":"OBSERVE"  "tool": "get_weather", "output":  "The temp of delhi is cloudy with 20c"},
     PLAN:{"step":"PLAN", "content": "Great, I go tthe weather info about Delhi"}
     PLAN:{"step":"OUTPUT", "content": "The current weather in delhi is 20 C with some cloudy"}
   

 """


print("\n\n\n")

message_history = [

        {"role":"system", "content": SYSTEM_PROMPT},


]

while True:
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

        if parsed_result.get("step") == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"🔎:{tool_to_call} ({tool_input})")
            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🔎:{tool_to_call} ({tool_input})= {tool_response}")
            message_history.append({"role":"developer", "content":json.dumps({
                "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response
            })})

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