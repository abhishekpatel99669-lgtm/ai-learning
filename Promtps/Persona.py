#Persona Based prompting
from dotenv import load_dotenv

from openai import OpenAI
import json
load_dotenv()

client = OpenAI()
SYSTEM_PROMTS="""
    You are an AI Persona Assistant named Abhishek Patel.
    You are an acting behalf of Abhishek Patel who is 22 years old.

    example:
    Q:Hey
    A:Hey,What's up!

    (100-150 example)

"""



response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMTS},
            {"role": "user", "content": "How are you"}
        ]
    )

print("Response:",response.choices[0].message.content)
