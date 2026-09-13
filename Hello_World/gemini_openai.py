"from dotenv import load_dotenv"

"load_dotenv()"

from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("open_api_key")
client = OpenAI()
response=client.chat.completions.create(
    model="gemini-3.6-flash",
    messages=[
        {"role":"system", "content":"you are expert in math only and only answer math related questions. That if the query is not related to math . just say sorry and do not answer that."},
        {"role":"user", "content":"hey you can help me solve the a+b whole square?"}
    ]
)
print(response.choices[0].message.content)