import openai
import json
import os
import pyttsx3
import speech_recognition as sr
import subprocess
# OpenAI API key (replace with your actual key)
openai.api_key = "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"

# Initialize Text-to-Speech
engine = pyttsx3.init()

# Initialize session context for maintaining conversation history
session_context = []

# Log file for saving assistant session
LOG_FILE = "assistant_logs.json"

# Voice Assistant: Speak a response
def speak(text):
    """Speak the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

# Voice Assistant: Listen for user input
def listen():
    """Listen for voice input using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Speech recognition is unavailable."

# Save session logs
def save_logs():
    """Save session context to a log file."""
    with open(LOG_FILE, "w") as log_file:
        json.dump(session_context, log_file, indent=4)

# Load session logs
def load_logs():
    """Load session context from a log file."""
    global session_context
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            session_context = json.load(log_file)

# Interact with OpenAI GPT
def gpt4_response(query):
    """Send a query to OpenAI GPT-4 and return the response."""
    try:
        session_context.append({"role": "user", "content": query})
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=session_context
        )
        assistant_response = response['choices'][0]['message']['content']
        session_context.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        return f"Error with GPT-4 API: {e}"

# Windows Task Automation
def execute_windows_task(command):
    """Execute common Windows tasks."""
    try:
        if "open notepad" in command:
            subprocess.Popen(["notepad.exe"])
            return "Opening Notepad."
        elif "open calculator" in command:
            subprocess.Popen(["calc.exe"])
            return "Opening Calculator."
        elif "list files" in command:
            files = os.listdir(".")
            return f"Current directory files: {', '.join(files)}"
        elif "create folder" in command:
            folder_name = "New_Folder"
            os.makedirs(folder_name, exist_ok=True)
            return f"Folder '{folder_name}' created."
        elif "delete folder" in command:
            folder_name = "New_Folder"
            os.rmdir(folder_name)
            return f"Folder '{folder_name}' deleted."
        else:
            return "I can't perform that task yet."
    except Exception as e:
        return f"Error executing task: {e}"

# Main Assistant Loop
def run_assistant():
    """Run the voice-activated assistant."""
    print("Voice-Activated Assistant Ready. Say 'exit' to quit.")
    speak("Voice-Activated Assistant Ready.")
    while True:
        # Get user input (voice or text fallback)
        user_input = listen()
        if not user_input or user_input.lower() in ["sorry, i didn't understand that", "speech recognition is unavailable"]:
            print("Fallback to text input.")
            user_input = input("You: ")

        print(f"You: {user_input}")

        if user_input.lower() == "exit":
            print("Assistant: Goodbye!")
            speak("Goodbye!")
            break
        elif user_input.lower() == "save":
            save_logs()
            print("Assistant: Logs saved successfully.")
            speak("Logs saved successfully.")
            continue
        elif user_input.lower() == "load":
            load_logs()
            print("Assistant: Logs loaded successfully.")
            speak("Logs loaded successfully.")
            continue

        # Check for specific commands
        if "open" in user_input or "list files" in user_input or "create folder" in user_input or "delete folder" in user_input:
            response = execute_windows_task(user_input)
        else:
            # ChatGPT interaction
            response = gpt4_response(user_input)

        print(f"Assistant: {response}")
        speak(response)

if __name__ == "__main__":
    run_assistant()
