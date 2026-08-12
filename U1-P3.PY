from sarvamai import SarvamAI
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()


client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)

user_prompt = input("Enter your prompt:")

start_time = time.time()

response = client.chat.completions(
    model="sarvam-105b",
    messages=[{'role':'user','content': user_prompt}]
    )

end_time = time.time()

AI_response = response
response_text = AI_response.choices[0].message.content
characters = len(response_text.split())
response_length = len(response_text)
word_count = len(response_text.split())
processing_time = end_time - start_time
model_name = "GPT-4"

if word_count <= 50:
    category = "Short"
elif word_count <= 150:
    category = "Medium"
else:
    category = "Long"


print("AI_response",AI_response)
print("Response Length:", response_length)
print("charaters:",characters)
print("Words:", word_count)
print("processing_time",processing_time)
print("Model Name:" , model_name)

