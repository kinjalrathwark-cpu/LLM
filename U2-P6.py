from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import asyncio
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("genai_api_key")
)

async def main():
    prompt = input("Enter your prompt: ")

    print("\nChoose response type:")
    print("1. Normal API Response")
    print("2. Streaming Response")

    choice = input("Enter choice (1/2): ")

    start_time = time.time()

    try:
        if choice == "1":
            #  Asynchronous normal API call 
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            end_time = time.time()
            total_time = end_time - start_time

            print("\nResponse:")
            print(response.text)

            print(f"\nTotal Response Time: {total_time:.2f} seconds")

        elif choice == "2":
            # Asynchronous streaming API call using Google GenAI SDK
            # Using chat session to maintain conversation history
            chat = client.aio.chats.create(model="gemini-3.8-flash")
            
            first_token_time = None
            chunks = 0

            print("\nResponse:")

            # Stream response token-by-token
            async for chunk in await chat.send_message_stream(prompt):
                if first_token_time is None:
                    first_token_time = time.perf_counter()
                
                chunks += 1
                if chunk.text:
                    print(chunk.text, end="", flush=True)

            end_time = time.time()
            print() # New line after stream completes

            #Display performance metrics
            time_to_first_token = first_token_time - start_time if first_token_time else 0.0
            total_time = end_time - start_time

            print(f"\nTime to First Token: {time_to_first_token:.2f} seconds")
            print(f"Total Response Time: {total_time:.2f} seconds")
            print(f"Streamed Chunks: {chunks}")

        else:
            print("Invalid choice! Please select 1 or 2.")

    except errors.APIError as e:
        #  Handle network/API errors gracefully
        print(f"\n[API Error]: A network or service interruption occurred: {e}")
    except Exception as e:
        print(f"\n[Error]: An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())

