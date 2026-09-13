from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

client = OpenAI()

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"user", "content":"2+2"}
    ]
)
print(response.choices[0].message.content)