import subprocess

# Helper function to run Git commands
def run_git_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = process.communicate()
    if stderr:
        print(f"Error: {stderr.decode()}")
    return stdout.decode(), stderr.decode()

# 1. Check Git status
def git_status():
    print("Checking Git status...")
    stdout, stderr = run_git_command("git status")
    print(stdout)

# 2. Stage all changes
def git_add():
    print("Staging changes...")
    stdout, stderr = run_git_command("git add .")
    print(stdout)

# 3. Commit changes
def git_commit(message):
    print(f"Committing changes with message: {message}")
    stdout, stderr = run_git_command(f'git commit -m "{message}"')
    print(stdout)

# 4. Push changes to remote
def git_push():
    print("Pushing changes to remote...")
    stdout, stderr = run_git_command("git push origin main")
    print(stdout)

# Main function to execute Git operations
if __name__ == "__main__":
    print("Starting Git automation...")
    try:
        git_status()
        git_add()
        commit_message = input("Enter commit message: ")
        git_commit(commit_message)
        git_push()
        print("Git operations completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
