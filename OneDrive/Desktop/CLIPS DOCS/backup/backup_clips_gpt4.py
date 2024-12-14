import subprocess

def run_clips(file_path):
    """
    Execute the CLIPS file using CLIPSDOS.EXE and return its output.
    """
    try:
        process = subprocess.run(
            ["C:/Program Files/SSS/CLIPS 6.4.1/CLIPSDOS.EXE", "-f2", file_path],
            capture_output=True,
            text=True
        )
        # Print raw outputs for debugging
        print("Raw Output:")
        print(process.stdout)
        print("Errors:")
        print(process.stderr)

        # Return the output for further processing
        return process.stdout.strip()
    except FileNotFoundError:
        return "Error: CLIPSDOS.EXE not found. Ensure the path is correct."
    except Exception as e:
        return f"Error occurred: {e}"

# Test the function
if __name__ == "__main__":
    clips_file = "C:/Users/salam/OneDrive/Desktop/CLIPS DOCS/OutcomeEvaluation.clp"
    print("Running CLIPS...")
    clips_output = run_clips(clips_file)
    print("\nCLIPS Output:\n", clips_output)

