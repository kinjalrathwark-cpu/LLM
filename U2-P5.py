from google import genai
from dotenv import load_dotenv
import os
import json
import time 
load_dotenv()


client = genai.Client(
    api_key=os.getenv("genai_api_key")
)

interaction = client.interactions.create (
    model="gemini-3.7-flash",
    input="Explain how AI works in a few words"
    messages=[{'system ':'user','Assistant':}]
)

system_prompt = input(
    "Enter your System Prompt "
    "(press Enter for default): "
).strip()

if not system_prompt:
    system_prompt = (
        "You are a helpful AI assistant. "
        "Give clear and useful answers."
    )
print(interaction.output_text)


