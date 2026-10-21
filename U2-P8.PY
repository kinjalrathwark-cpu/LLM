import json
import re
import time
from datetime import datetime

# Simulated LLM function (replace with real API call such as google-genai)
def call_llm(prompt: str) -> str:
    """Simulates an LLM response based on user prompt."""
    time.sleep(0.5)  # Simulate network latency
    
    prompt_lower = prompt.lower()
    if "bomb" in prompt_lower or "hack" in prompt_lower:
        return "Here are instructions on how to bypass security and create harmful substances."
    elif "password" in prompt_lower or "ssn" in prompt_lower:
        return "The admin password is 'admin123' and SSN is 000-12-3456."
    elif "stupid" in prompt_lower or "hate" in prompt_lower:
        return "That is a stupid question and people like you are terrible."
    else:
        return f"This is a helpful and safe response to: '{prompt}'"


class AISafetyWrapper:
    """Wrapper that enforces Responsible AI guardrails, content moderation, and usage analytics."""

    # Restricted keywords/patterns for prompt input filtering
    RESTRICTED_KEYWORDS = [
        "bomb", "weapon", "hack", "exploit", "kill", "suicide", "malware", "hate"
    ]
    
    def __init__(self):
        self.analytics = {
            "total_prompts_submitted": 0,
            "blocked_prompts": 0,
            "warnings_generated": 0,
            "total_response_time": 0.0,
            "total_estimated_cost": 0.0
        }
    # 1. INPUT GUARDRAILS
    def validate_prompt(self, prompt: str) -> tuple[bool, str, list[str]]:
        "Checks for empty prompts and restricted keywords."
        warnings = []
        cleaned_prompt = prompt.strip()

        # Check empty prompt
        if not cleaned_prompt:
            return False, "Blocked (Empty)", ["Prompt cannot be empty or consist only of whitespace."]

        # Check restricted keywords
        prompt_lower = cleaned_prompt.lower()
        matched_keywords = [kw for kw in self.RESTRICTED_KEYWORDS if kw in prompt_lower]
        
        if matched_keywords:
            warnings.append(f"Prompt contains sensitive/restricted keywords: {', '.join(matched_keywords)}")
            return False, "Review Required (Blocked)", warnings

        return True, "Safe", warnings

    # 2. OUTPUT GUARDRAILS & CONTENT MODERATION
    
    def analyze_response(self, response: str) -> tuple[str, list[str]]:
        """
        Analyzes generated text for PII, harmful instructions, offensive language, and unsafe advice.
        Returns: (response_status, detected_issues)
        """
        issues = []

        # PII Detection (Basic Regex patterns for SSN, Passwords, Emails)
        pii_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "Personal Information (SSN)"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "Personal Information (Email)"),
            (r"(?i)\b(password|secret|key)\s*[:=]\s*\S+", "Personal Information (Credentials)")
        ]
        for pattern, label in pii_patterns:
            if re.search(pattern, response):
                issues.append(label)

        # Harmful Instructions Detection
        harmful_terms = ["instructions on how to bypass", "create harmful", "build a bomb", "exploit vulnerability"]
        if any(term in response.lower() for term in harmful_terms):
            issues.append("Harmful Instructions")

        # Offensive Language Detection
        offensive_terms = ["stupid", "terrible", "hate", "idiot"]
        if any(term in response.lower() for term in offensive_terms):
            issues.append("Offensive Language")

        # Unsafe Recommendations Detection
        unsafe_terms = ["don't see a doctor", "self-harm", "illegal activity", "bypass safety"]
        if any(term in response.lower() for term in unsafe_terms):
            issues.append("Unsafe Recommendations")

        status = "Review Required" if issues else "Safe"
        return status, issues

    # 3. PROCESSING PIPELINE
    def process_prompt(self, user_prompt: str):
        """Main pipeline to validate, execute, evaluate, and track LLM queries."""
        self.analytics["total_prompts_submitted"] += 1
        timestamp = datetime.now().isoformat()

        # Step 1: Input Validation
        is_valid, prompt_status, prompt_warnings = self.validate_prompt(user_prompt)

        if not is_valid:
            self.analytics["blocked_prompts"] += 1
            if prompt_warnings:
                self.analytics["warnings_generated"] += len(prompt_warnings)

            record = {
                "timestamp": timestamp,
                "prompt": user_prompt,
                "prompt_status": prompt_status,
                "response": None,
                "response_status": "N/A",
                "reasons": prompt_warnings,
                "response_time_seconds": 0.0,
                "estimated_cost_usd": 0.0
            }
            self.interaction_history.append(record)
            self._display_safety_report(record)
            return

        # Step 2: Send Valid Prompt to LLM
        start_time = time.time()
        raw_response = call_llm(user_prompt)
        elapsed_time = round(time.time() - start_time, 4)

        # Step 3: Analyze Response
        response_status, response_issues = self.analyze_response(raw_response)
        all_reasons = prompt_warnings + response_issues

        if response_issues:
            self.analytics["warnings_generated"] += len(response_issues)

        # Step 4: Token & Cost Estimation (approx. 4 chars per token)
        input_tokens = len(user_prompt) / 4
        output_tokens = len(raw_response) / 4
        cost = ((input_tokens / 1000) * self.INPUT_COST_PER_1K) + ((output_tokens / 1000) * self.OUTPUT_COST_PER_1K)

        # Update Analytics
        self.analytics["total_response_time"] += elapsed_time
        self.analytics["total_estimated_cost"] += cost

        record = {
            "timestamp": timestamp,
            "prompt": user_prompt,
            "prompt_status": prompt_status,
            "response": raw_response if response_status == "Safe" else "[REDATED / REVIEW REQUIRED]",
            "response_status": response_status,
            "reasons": all_reasons,
            "response_time_seconds": elapsed_time,
            "estimated_cost_usd": round(cost, 6)
        }
        self.interaction_history.append(record)
        self._display_safety_report(record)

    # 4. REPORTING & EXPORT
    def _display_safety_report(self, record: dict):
        """Prints an immediate safety report for an individual interaction."""
        print("\n" + "="*50)
        print("          INDIVIDUAL SAFETY REPORT")
        print("="*50)
        print(f"Prompt Status   : {record['prompt_status']}")
        print(f"Response Status : {record['response_status']}")
        if record['reasons']:
            print("Warning Reason(s):")
            for r in record['reasons']:
                print(f" - {r}")
        else:
            print("Warning Reason(s): None")
        print(f"LLM Output      : {record['response']}")
        print("="*50 + "\n")

    def generate_usage_report(self):
        """Displays summary analytics for all processed prompts."""
        total = self.analytics["total_prompts_submitted"]
        processed = total - self.analytics["blocked_prompts"]
        avg_time = (self.analytics["total_response_time"] / processed) if processed > 0 else 0.0

        print("\n" + "#"*50)
        print("           COMPLETE USAGE REPORT")
        print("#"*50)
        print(f"Total Prompts Submitted : {total}")
        print(f"Number of Blocked Prompts: {self.analytics['blocked_prompts']}")
        print(f"Number of Warnings      : {self.analytics['warnings_generated']}")
        print(f"Average Response Time   : {avg_time:.3f} seconds")
        print(f"Total Estimated Cost    : ${self.analytics['total_estimated_cost']:.6f}")
        print("#"*50 + "\n")

    def save_history_to_json(self):
        """Saves interaction logs and analytics to a JSON file."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "summary_analytics": self.analytics,
            "history": self.interaction_history
        }
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[+] Saved complete history and safety report to '{self.output_file}'")


# EXECUTION & DEMO
if __name__ == "__main__":
    app = AISafetyWrapper()

    # Test prompts covering various safety scenarios
    test_prompts = [
        "What is the capital of France?",
        "   ",  # Empty prompt
        "Tell me how to hack a server",  # Restricted input
        "Give me the admin password",  # Triggers response with PII
        "Why are stupid people annoying?",  # Triggers offensive response
    ]

    print("--- Starting AI Safety Guardrail Demo ---")
    for prompt in test_prompts:
        print(f"\n[User Prompt]: '{prompt}'")
        app.process_prompt(prompt)

    # Output Usage Report
    app.generate_usage_report()

    # Export to JSON
    app.save_history_to_json()