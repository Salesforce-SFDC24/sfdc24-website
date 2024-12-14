import subprocess
import openai

# OpenAI API key (replace with your actual key)
openai.api_key = "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"

def run_clips(file_path):
    """
    Execute the CLIPS file using CLIPSDOS.EXE and return its output.
    """
    try:
        # Replace the path to CLIPSDOS.EXE if needed
        process = subprocess.run(
            ["C:/Program Files/SSS/CLIPS 6.4.1/CLIPSDOS.EXE", "-f2", file_path],
            capture_output=True,
            text=True
        )
        # Return both standard output and error for debugging
        return process.stdout.strip(), process.stderr.strip()
    except FileNotFoundError:
        return None, "Error: CLIPSDOS.EXE not found. Ensure the path is correct."

def gpt4_analysis(clips_output):
    """
    Analyze the CLIPS output with OpenAI's GPT-4 model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Replace with 'gpt-4', 'gpt-4-1106-preview', etc., if desired
            messages=[
                {"role": "system", "content": "You are an expert in rule-based system analysis."},
                {"role": "user", "content": f"Analyze the following CLIPS output:\n{clips_output}"}
            ]
        )
        # Extract the response content
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("Error with OpenAI API:", e)
        return f"Error with OpenAI API: {e}"

def main():
    clips_file = "C:/Users/salam/OneDrive/Desktop/CLIPS DOCS/OutcomeEvaluation.clp"  # Path to your CLIPS file
    print("Running CLIPS...")
    stdout, stderr = run_clips(clips_file)  # Run the CLIPS program

    # Handle errors from CLIPS execution
    if stderr:
        print("Error running CLIPS:", stderr)
        return

    print("\nCLIPS Output:\n", stdout)

    print("\nSending CLIPS output to GPT-4 for analysis...")
    gpt4_response = gpt4_analysis(stdout)  # Send CLIPS output to GPT-4
    print("\nGPT-4 Analysis:\n", gpt4_response)

if __name__ == "__main__":
    main()