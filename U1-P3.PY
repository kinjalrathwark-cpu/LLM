from google import genai
from dotenv import load_dotenv
import time
import os 

load_dotenv()

client = genai.Client(
    api_key= os.getenv("GEMINI_API_KEY")
)

user_prompt = input("Enter Text:")

start=time.time()

response = client.models.generate_content(
    model="gemini-3.6-flash",     
    contents=user_prompt
)

end=time.time()

print("gemini response")
print(response.text)

total_time=end-start

characters=len(user_prompt)
word=len(user_prompt.split())

print("gemini response")
print(response.text)


print(f"characters lenth:{characters}")
print(f"word lenth:{word}")
print(f"Total Processing Time:{total_time}")
print("Model Name:gemini-3.6-flash") 


if word<50:
    print("Short")
elif word<=150:
    print("Medium")
else:
    print("Long")

print(response)
