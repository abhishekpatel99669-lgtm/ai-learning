
from dotenv import load_dotenv
# from fastapi import requests
from openai import OpenAI
import requests
import json
from pydantic import BaseModel,Field
from typing import Optional
import os
load_dotenv()

client = OpenAI()

def run_command(cmd:str):
     result=os.system(cmd)
     return result

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}"
    return f"something went  wrong"

avlable_tool={
     "get_weather":get_weather,
     "run_command":run_command
     
}


SYSTEM_PROMTS="""
   You are an expert AI assistant in resolving user queries using chai of thought.
   You work on START,PLAN and OUTPUT steps.
   You need to first PLAN what needs to be done.The plan can be multiple steps.
   Once you have enough PLAN has been done, Finally you can give the OUTPUT.
   You can also call a tool if required from the list of available tools.
   For every tool call wait for the abserve step Which is the output from the called tool.

   Rules:
   -Strictly folloe the given json output formet.
   -Only run one step at a time.
   -The sequence of step is START(where user gives an input),PLAN(That can be multiple times),and Finally OUTPUT(ehich is going to the displaysd to  the user).

   Output JSON Formet:
   {"step": "START"|"PLAN"|"OUTPUT" |"TOOL", "content": "string", "tool": "sting", "input":"string"}

   Available Tools:
   -Get weather(city:str): Takes city name as an input string and returns the weather info about the city.
   -run_command(cmd:str):Takes a system liunx command as string and excutes the command on user's system and return the output from the command.
    Example-1:
   START: Hey! you can solve 2+3*5-8/4
   PLAN:{"step": "PLAN", "content": "seems like usre is interested maths problem."}
   PLAN:{"step": "PLAN", "content": looking at the problem, we should solve this BODMAS method"."}
   PLAN:{"step": "PLAN", "content": "Yes, the is corret thing to be done here.}
   PLAN:{"step": "PLAN", "content": "first we must multiply 3*5 = 15"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 2+15-8/4"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the division 8/4 = 2"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 2+12-2"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the addition 2+12=14"}
   PLAN:{"step": "PLAN", "content":"Now the new equation is 14-2"}
   PLAN:{"step": "PLAN", "content":"Now we must perform the subtraction 14-2=12"}
   PLAN:{"step": "PLAN", "content":"Great! we have solved and finaly left with the answer 12"}
   OUTPUT:{"step": "OUTPUT", "content": "12"}

   Example-2:
      START: What is the weather of Delhi?
      PLAN:{"step": "PLAN", "content": "seems like usre is interested in getting a weather of Delhi in India."}
      PLAN:{"step": "PLAN", "content": "Lets see if we have any available tool from the list of available tools"}
      PLAN:{"step": "PLAN", "content": "Great, we have get_weather tool available for this query."}
      PLAN:{"step": "PLAN", "content": "I need to call get_weather tool for Delhi as input for city."}
      PLAN:{"step": "TOOL", "tool":"get_weather", "input": "delhi"}
      PLAN:{"step": "OBSERVE", "tool":"get_weather", "input":" The temp of delhi is cloudy with 20'C"}
      PLAN:{"step": "PLAN", "content":"Great, I got the weather info about Delhi"}
     
      OUTPUT:{"step": "OUTPUT", "content": "The current weather in delhi is 20'C with some cloudy sky."}
   
   
   


"""
print("n/n/n")

class MyOutputFormet(BaseModel):
    step: str = Field(..., description="The ID of The step. Example:PLAN,OUTPUT,TOOL etc")
    content:Optional[str]=Field(None,discription="The optional string content for the step.")
    tool:Optional[str]=Field(None,discription="The ID of tool to call")
    input:Optional[str]=Field(None,discription="The input params for the tool")

message_history=[
    {"role": "system", "content": SYSTEM_PROMTS},
]

user_query=input(" 👉 ")

message_history.append({"role": "user", "content": user_query})

while True:
    
    
    response=client.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=MyOutputFormet,
        messages=message_history
        )

    raw_result=(response.choices[0].message.content)
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result=(response.choices[0].message.parsed)

    if parsed_result.step=="START":
        print("🔥", parsed_result.content)
        continue

    if parsed_result.step=="TOOL":
        tool_to_call=parsed_result.tool
        tool_to_input=parsed_result.input
        print(f"⛏️:{tool_to_call} ({tool_to_input})")

        tool_response=avlable_tool[tool_to_call](tool_to_input)
        print(f"⛏️:{tool_to_call} ({tool_to_input})")

        message_history.append({"role":"developer", "content":json.dumps(
             {"step":"OBSERVE","tool":"tool_to_call","input":"tool_input","output":"tool_response"}
        )})
        continue
             
        


    if parsed_result.step=="PLAN":
        print("🧠", parsed_result.content)
        continue
    if parsed_result.step=="OUTPUT":
            print("🤖", parsed_result.content)
            break

print("n/n/n")
