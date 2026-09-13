"from dotenv import load_dotenv"
import os
"load_dotenv()"

from openai import OpenAI



client = OpenAI(
    api_key="AQ.Ab8RN6KjAcZNb_WN7_wP0GIkjgLP5vKbaKafWeewWiSdIYSr1g4",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
# direct giving the instruvtion to the model and example to the model

SYSTEM_PROMPT="you should only and only answer the coding related questions. do not answer anything else. your name is alexa . If user say something other then coding,just say sorry and do not answer that."


response=client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role":"system", "content":"SYSTEM_PROMPT"},
        {"role":"user", "content":"hey,add two number"}
    ]
)
print(response.choices[0].message.content) 



