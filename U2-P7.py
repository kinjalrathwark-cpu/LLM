from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import csv
import time
import json

load_dotenv()

# Initialize the Google GenAI client
client = genai.Client(
    api_key=os.getenv("genai_api_key")
)

def estimate_cost(total_tokens, model_name):
    # Nominal pricing estimation formula per 1M tokens (adjust based on actual model tier)
    return (total_tokens / 1_000_000) * 0.10

def main():
    print("=== Batch Prompt Processor with Google GenAI ===")
    
    # User inputs for configuration matching your prompt flow
    model_name = input("Enter Model Name [gemini-3.8-flash]: ").strip() or "gemini-3.8-flash"
    
    try:
        temperature = float(input("Enter temperature (0-1) [0.7]: ") or 0.7)
        top_p = float(input("Enter Top P (0-1) [1.0]: ") or 1.0)
        max_tokens = int(input("Enter Maximum Tokens (<=500) [100]: ") or 100)
    except ValueError:
        temperature, top_p, max_tokens = 0.7, 1.0, 100

    csv_filename = "prompts.csv"
    
    # 1. Check and read prompts from CSV
    if not os.path.exists(csv_filename):
        print(f"\n[Error] CSV file '{csv_filename}' not found.")
        print("Please create 'prompts.csv' with a 'prompt' column before running.")
        return

    prompts = []
    try:
        with open(csv_filename, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "prompt" in row:
                    prompts.append(row["prompt"])
                elif row:
                    # Fallback to first column if 'prompt' header isn't explicitly named
                    prompts.append(list(row.values())[0])
    except Exception as e:
        print(f"\n[Error reading CSV]: {e}")
        return

    if not prompts:
        print("\nNo prompts found to process. Exiting.")
        return

    print(f"\nLoaded {len(prompts)} prompts. Starting batch processing...\n")

    results = []
    successful_requests = 0
    failed_requests = 0
    total_tokens_used = 0
    total_cost = 0.0

    # 2. Iterate through prompts one by one
    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}/{len(prompts)}] Processing status: Running...")
        start_time = time.time()
        
        try:
            config = {
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": max_tokens,
            }

            # API Call
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 3. Extract actual token usage or fallback estimate
            usage = getattr(response, "usage_metadata", None)
            tokens = usage.total_token_count if usage and hasattr(usage, "total_token_count") else len(prompt.split()) + len(response.text.split())
            
            cost = estimate_cost(tokens, model_name)
            
            successful_requests += 1
            total_tokens_used += tokens
            total_cost += cost

            result_text = response.text.strip()
            print(f"  -> Status: Success | Time: {response_time:.2f}s | Tokens: {tokens} | Cost: ${cost:.6f}")

            results.append({
                "prompt": prompt,
                "response": result_text,
                "status": "Success",
                "response_time_seconds": round(response_time, 2),
                "token_count": tokens,
                "estimated_cost_usd": round(cost, 6)
            })

        except errors.APIError as e:
            end_time = time.time()
            response_time = end_time - start_time
            failed_requests += 1
            print(f"  -> Status: Failed [API Error] | Time: {response_time:.2f}s | Error: {e}")
            results.append({
                "prompt": prompt,
                "response": str(e),
                "status": "Failed",
                "response_time_seconds": round(response_time, 2),
                "token_count": 0,
                "estimated_cost_usd": 0.0
            })
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            failed_requests += 1
            print(f"  -> Status: Failed [Error] | Time: {response_time:.2f}s | Error: {e}")
            results.append({
                "prompt": prompt,
                "response": str(e),
                "status": "Failed",
                "response_time_seconds": round(response_time, 2),
                "token_count": 0,
                "estimated_cost_usd": 0.0
            })

        # 4. Respect API rate limits with a short polite delay between requests
        time.sleep(1.0)

    # 5. Generate Summary Report metrics
    summary = {
        "total_prompts_processed": len(prompts),
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "total_estimated_token_usage": total_tokens_used,
        "total_estimated_api_cost_usd": round(total_cost, 6)
    }

    print("\n" + "="*45)
    print("           BATCH SUMMARY REPORT")
    print("="*45)
    print(f"Total Prompts Processed : {summary['total_prompts_processed']}")
    print(f"Successful Requests     : {summary['successful_requests']}")
    print(f"Failed Requests         : {summary['failed_requests']}")
    print(f"Total Token Usage       : {summary['total_estimated_token_usage']}")
    print(f"Total Estimated Cost    : ${summary['total_estimated_api_cost_usd']:.6f}")
    print("="*45)

    # 6. Export results and summary to CSV and JSON files
    output_csv = "batch_results.csv"
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["prompt", "response", "status", "response_time_seconds", "token_count", "estimated_cost_usd"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\n[Export]: Detailed results saved to '{output_csv}'")
    except Exception as e:
        print(f"[Export Error]: Could not save CSV: {e}")

    output_json = "summary_report.json"
    try:
        with open(output_json, mode="w", encoding="utf-8") as f:
            json.dump({"summary": summary, "results": results}, f, indent=4)
        print(f"[Export]: Summary report saved to '{output_json}'")
    except Exception as e:
        print(f"[Export Error]: Could not save JSON: {e}")

if __name__ == "__main__":
    main()
