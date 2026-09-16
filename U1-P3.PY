from google import genai
from dotenv import load_dotenv
import time

api_key = input("Enter API Key   : ").strip()

client = genai.Client(api_key=api_key)

user_prompt = input("Enter Text:")

start_time=time.time()
response = client.models.generate_content(
    model="gemini-3.6-flash",     
    contents=user_prompt
)
end_time=time.time()
total_time=end_time-start_time


# print("gemini response")
# print(response.text)

ai_respone=response.text
characters=len(response.text)
word=len(response.text.split())



if word<=50:
    category = "Short"
elif word<=150:
    category = "Medium"
else:
    category = "Long"

finish_reason = response.candidates[0].finish_reason if response.candidates else "N/A"

print(f"\nUser Promt :             {user_prompt}")
print(f"AI Response :  \n          {ai_respone}")
print(f"characters lenth:        {characters}")
print(f"word lenth:              {word}")
print(f"Response Category       {category}")
print(f"Total Processing Time:    {total_time}")
print("Model Name:                gemini-3.6-flash") 
print(f"Finish Reason            {finish_reason}")


