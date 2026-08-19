from sarvamai import SarvamAI
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

api_key = input("Enter your APY KEY")
model_name = input("Enter Model Name")
prompt = input('Enter your prompt')
temperature = float(input("Enter Temperature"))
top_p = float(input("Enter Top-p:"))
maximum_tokens = input("Enter Maximum tokens") 
stop_sequence = input("Enter  stop Sequence ")

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY") 
)
data = { 
    "model_name" : model_name,
    "prompt" : prompt,
    "temperature" : temperature,
    "top-p" : top_p,
    "maximum_tokens" : maximum_tokens,
    "stop_sequence" : stop_sequence
}
if stop_sequence:
    data["stop"] = stop_sequence

# SEND PROMT TO LLM , sned request
start_time = time.time()
response = client.chat.completions(
    model= model_name,
    input = prompt
)
end_time = time.time()


#Generated Response
Generated_Response = response
response_time = end_time - start_time # response time 

response_text = Generated_Response.choices[0].message.content
print("generated response")
print(Generated_Response)


output_data = {
    "model_name" : model_name,
    "prompt" : prompt,
    "temperature" : temperature,
    "top-p" : top_p,
    "maximum_tokens" : maximum_tokens,
    "stop_sequence" : stop_sequence,
    "response_time" : response_time
}

