

import openai
import json
import os

# Replace with your actual OpenAI API key
openai.api_key = "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"

# Log file for saving conversation history
LOG_FILE = "assistant_logs.json"

def get_gpt_response(user_input):
    """
    Get a response from GPT-4 for the given user input.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error with GPT-4 API: {str(e)}"

def save_logs(conversation_log):
    """
    Save the conversation log to a file.
    """
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(conversation_log, f, indent=4)
        print("Logs saved successfully.")
    except Exception as e:
        print(f"Error saving logs: {str(e)}")

def load_logs():
    """
    Load conversation logs from a file.
    """
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        else:
            print("No logs found. Starting fresh.")
            return []
    except Exception as e:
        print(f"Error loading logs: {str(e)}")
        return []

def main():
    """
    Main function to run the assistant.
    """
    print("Welcome to your GPT-4 Assistant! Type 'exit' to quit.")
    print("Type 'save' to save logs or 'load' to load logs.")

    conversation_log = []

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "save":
            save_logs(conversation_log)
        elif user_input.lower() == "load":
            conversation_log = load_logs()
            print("Logs loaded.")
        else:
            assistant_response = get_gpt_response(user_input)
            print(f"Assistant: {assistant_response}")

            # Save the interaction in the log
            conversation_log.append({"user": user_input, "assistant": assistant_response})

if __name__ == "__main__":
    main()
