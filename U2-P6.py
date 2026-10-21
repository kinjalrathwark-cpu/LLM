from google import genai
from dotenv import load_dotenv
import os
import asyncio
import time
load_dotenv()

client = genai.Client(
    api_key=os.getenv("genai_api_key")
)

# prompt = input("Enter your prompt: ")
# print("\nChoose response type:")
# print("1. Normal API Response")
# print("2. Streaming Response")

# choice = input("Enter choice (1/2): ")
async def main():  #function start
      
    prompt = input("Enter your prompt: ")

    print("\nChoose response type:")
    print("1. Normal API Response")
    print("2. Streaming Response")

    choice = input("Enter choice (1/2): ")

    start_time = time.time()

    if choice == "1":
            # Normal asynchronous response
            response = await client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            end_time = time.time()
            total_time = end_time -  start_time

            print("\nResponse:")
            print(response.output_text)

            print(f"\nTotal Response Time: {total_time:.2f} seconds")

    elif choice == "2":
            # Asynchronous streaming response
            stream = await client.aio.models.generate_content_stream(  #await client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
                stream=True
            )

            first_token_time = None
            chunks = 0

            print("\nResponse:")

            async for event in stream:
                if event.type == "response.output_text.delta":

                    if first_token_time is None:
                        first_token_time = time.perf_counter()

                    chunks += 1
                    print(event.delta, end="", flush=True)

            end_time = time.time()

            print()

            total_response_time = first_token_time - start_time
            total_time = end_time - start_time

            print(f"\nTime to First Token: {total_response_time:.2f} seconds")
            print(f"Total Response Time: {total_time:.2f} seconds")
            print(f"Streamed Chunks: {chunks}")

    else:
            print("Invalid choice!")

if __name__ == "__main__":
    asyncio.run(main())   #function run 
