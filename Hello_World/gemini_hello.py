# from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
# response = Client.models.generate.content(
#     model="gemini-2.5-flash", content="explain how AI works in a few words"
# )

# print(response.txt)
from google import genai

client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input="Explain how AI works in a few words"
)

print(interaction.output_text)
