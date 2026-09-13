# few-sort Prompting
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI



import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("gemini_api_key")
# direct giving the instruvtion to the model and example to the model
client = OpenAI()
PROMPT="""
you should only and only answer the coding related questions. do not answer anything else. your name is alexa . If user say something other then coding,just say sorry and do not answer that.

Rules:
-Strictiy follew the output in json format

Output formet:
{{
"code": "string", or null
"is codeingquestion": boolean
}}

example:
Q: can you explain the a+b whole square?
A:{{"Code": null, "is_codeingquestion": false}}

Q: Hey, write a code in python adding two numbers?
A:{{"Code": "def add(a,b):\n    return a+b", "is_codeingquestion": true}}

"""
response=client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
            {"role":"system", "content":"SYSTEM_PROMPT"},
            {"role":"user", "content":"hey, can you code in python"}
       ]
)

print(response.choices[0].message.content)





