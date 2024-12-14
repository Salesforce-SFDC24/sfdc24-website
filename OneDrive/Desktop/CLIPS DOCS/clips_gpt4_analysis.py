import subprocess
import openai
import matplotlib.pyplot as plt

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
            model="gpt-4-turbo",  # Replace with your preferred GPT model
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

def visualize_scores(clips_output, save_path="contributor_scores.png"):
    """
    Parse the CLIPS output and generate a bar chart for contributor scores.
    Save the chart as an image file if needed.
    """
    contributors = []
    scores = []

    # Parse the CLIPS output
    for line in clips_output.split("\n"):
        if "Score:" in line:
            parts = line.split()
            contributors.append(parts[1])  # e.g., Contributor 1
            scores.append(float(parts[3]))  # e.g., Score value

    # Plot the scores
    plt.bar(contributors, scores, color='skyblue')
    plt.xlabel("Contributors")
    plt.ylabel("Scores")
    plt.title("Contributor Performance Scores")
    plt.savefig(save_path)  # Save the chart as an image
    print(f"Chart saved as {save_path}")
    plt.show()

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

    # Save the analysis to a text file
    with open("gpt4_analysis.txt", "w") as file:
        file.write("CLIPS Output:\n")
        file.write(stdout + "\n\n")
        file.write("GPT-4 Analysis:\n")
        file.write(gpt4_response)
    print("Analysis saved to gpt4_analysis.txt")

    # Visualize the scores
    visualize_scores(stdout)

if __name__ == "__main__":
    main()