
import os
from dotenv import load_dotenv

from openai import OpenAI
import json
load_dotenv()

client = OpenAI()

SYSTEM_PROMTS="""
   You are an expert AI assistant in resolving user queries using chai of thought.
   You work on START,PLAN and OUTPUT steps.
   You need to first PLAN what needs to be done.The plan can be multiple steps.
   Once you have enough PLAN has been done, Finally you can give the OUTPUT.

   Rules:
   -Strictly folloe the given json output formet.
   -Only run one step at a time.
   -The sequence of step is START(where user gives an input),PLAN(That can be multiple times),and Finally OUTPUT(ehich is going to the displaysd to  the user).

   Output JSON Formet:
   {"step": "START"|"PLAN"|"OUTPUT", "content": "string"}
   Example:
   START: Hey! you can solve 2+3*5-8/4
   PLAN:{"step": "PLAN", "content": "seems like usre is interested maths problem".}
   PLAN:{"step": "PLAN", "content": "looking at the problem, we should solve this BODMAS method."}
   PLAN:{"step": "PLAN", "content": "Yes, the is corret thing to be done here."}
   PLAN:{"step": "PLAN", "content": "first we must multiply 3*5 = 15"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 2+15-8/4"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the division 8/4 = 2"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 2+12-2"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the addition 2+12=14"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 14-2"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the subtraction 14-2=12"}
   PLAN:{"step": "PLAN", "content":"Great! we have solved and finaly left with the answer 12"}
   OUTPUT:{"step": "OUTPUT", "content": "12"}


"""
print("n/n/n")

message_history=[
    {"role": "system", "content": SYSTEM_PROMTS},
]

user_query=input(" 👉 ")

message_history.append({"role": "user", "content": user_query})

while True:
    
    
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
        )

    raw_result=(response.choices[0].message.content)
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result=json.loads(raw_result)

    if parsed_result.get("step")=="START":
        print("🔥", parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="PLAN":
        print("🧠", parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

print("n/n/n")


 




