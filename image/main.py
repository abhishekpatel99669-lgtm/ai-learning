from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content":[
                {"type":"text", "text": "generate a caption for this image in about 60 woerds."},
                {"type":"image_url", "image_url":{"url": "https://images.pexels.com/photos/2102416/pexels-photo-2102416.jpeg"}}

            ]
        }
    ]
)

print(response.choices[0].message.content)