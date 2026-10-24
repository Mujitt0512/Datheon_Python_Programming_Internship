import datetime
import json
import os
import sys

DATASET_FILENAME = "sample_faq.json"

def load_faq_dataset(filename):
    """Loads questions and responses dynamically from an external JSON dataset."""
    if not os.path.exists(filename):
        print(f"[!] Error: The dataset file '{filename}' was not found in the directory.")
        print("    Please ensure 'faq.json' is created in the same folder as chatbot.py.")
        sys.exit(1)
        
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"[+] Successfully loaded FAQ dataset from '{filename}'.")
            return data
    except json.JSONDecodeError:
        print(f"[!] Error: '{filename}' contains invalid JSON formatting.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Unexpected error loading dataset: {e}")
        sys.exit(1)

def get_current_time_str():
    """Returns current date and time as a formatted string."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y — %I:%M %p")

def evaluate_math_expression(query):
    """Safely evaluates basic arithmetic queries."""
    for prefix in ["calculate", "solve", "math", "what is", "compute"]:
        if query.startswith(prefix):
            query = query.replace(prefix, "", 1).strip()
            
    allowed_chars = set("0123456789+-*/(). %")
    if all(char in allowed_chars for char in query):
        try:
            result = eval(query)
            return f"The result of {query} is **{result}**."
        except ZeroDivisionError:
            return "[!] Error: Division by zero is undefined."
        except Exception:
            return "I couldn't compute that expression. Please check your syntax."
    return None

def get_bot_response(user_input, faq_data):
    """Processes user input, searches the JSON dataset safely, and handles utilities."""
    cleaned_input = user_input.lower().strip()

    # 1. Handle Exit Commands
    if cleaned_input in ["exit", "quit", "bye", "goodbye"]:
        return "EXIT"

    # 2. Handle Time/Date Utility
    elif any(phrase in cleaned_input for phrase in ["time", "date", "day is it", "clock"]):
        return f"Current Local Date & Time: {get_current_time_str()}"

    # 3. Handle Math Calculation Utility
    elif any(prefix in cleaned_input for prefix in ["calculate", "solve", "math", "what is", "compute"]) and any(op in cleaned_input for op in ["+", "-", "*", "/", "%"]):
        math_response = evaluate_math_expression(cleaned_input)
        if math_response:
            return math_response

    # 4. Safely check queries against loaded JSON dataset (Handles both list and dict structures)
    if isinstance(faq_data, dict):
        entries = faq_data.values()
    elif isinstance(faq_data, list):
        entries = faq_data
    else:
        entries = []

    for entry in entries:
        if isinstance(entry, dict):
            keywords = entry.get("keywords", [])
            response_text = entry.get("response", "")
            if any(keyword in cleaned_input for keyword in keywords):
                return response_text

    # 5. Handle Help Command
    if "help" in cleaned_input or "commands" in cleaned_input:
        return (
            "Here is what I can help you with:\n"
            "  • **Dataset FAQs**: Ask questions based on your loaded dataset topics (e.g., hello, internship, deadline).\n"
            "  • **Time/Date Queries**: Ask 'what time is it?'\n"
            "  • **Math Calculations**: Ask 'calculate 150 * 4'\n"
            "  • **Exit**: Type 'exit' or 'quit' to close."
        )

    # 6. Graceful Fallback for Unrecognized Queries
    return "I'm sorry, I didn't quite catch that. Type **'help'** to view available options or check your phrasing."

def run_chatbot():
    """Runs the interactive terminal chat loop."""
    faq_data = load_faq_dataset(DATASET_FILENAME)

    print("\n" + "=" * 55)
    print("      DATHEON RULE-BASED TERMINAL ASSISTANT")
    print("=" * 55)
    print("Type your questions below. Type 'help' for options or 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            response = get_bot_response(user_input, faq_data)

            if response == "EXIT":
                print("\nAssistant: Goodbye! Have a great day ahead. Shutting down...\n")
                break

            print(f"\nAssistant: {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\nAssistant: Session interrupted. Goodbye!\n")
            break

if __name__ == "__main__":
    run_chatbot()