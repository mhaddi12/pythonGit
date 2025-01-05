import os
import subprocess
from datetime import date, datetime

def is_git_repo():
    """Check if the current directory is a Git repository."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def run_command(command, error_message):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"{error_message}\nError: {e.stderr.strip()}")
        exit(1)

def git_commit_and_push(commit_message):
    if not is_git_repo():
        print("This is not a Git repository. Please navigate to a valid Git repository and try again.")
        exit(1)

    # Check the current branch
    branch = run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        "Failed to get the current branch. Are you inside a Git repository?"
    )
    print(f"Current branch: {branch}")

    # Pull latest changes to avoid conflicts
    print("Pulling latest changes...")
    run_command(["git", "pull", "origin", branch], "Failed to pull changes from the remote repository.")

    # Check for changes before staging and committing
    status = run_command(["git", "status", "--porcelain"], "Failed to check repository status.")
    if not status:
        print("No changes to commit. Exiting.")
        return

    # Stage all changes
    print("Staging all changes...")
    run_command(["git", "add", "."], "Failed to stage changes.")

    # Commit changes
    print("Committing changes...")
    run_command(["git", "commit", "-m", commit_message], "Failed to commit changes. Ensure there are changes to commit.")

    # Push changes
    print("Pushing changes to the remote repository...")
    run_command(["git", "push", "origin", branch], "Failed to push changes to the remote repository.")
    print(f"Changes pushed successfully to branch '{branch}'.")

    # Update README.md with current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    readme_path = "README.md"
    
    # Ensure README.md exists before appending
    if os.path.exists(readme_path):
        with open(readme_path, "a") as readme_file:
            readme_file.write(f"\nUpdated on: {current_datetime}\n")
    else:
        print(f"README.md not found. Skipping update.")

if __name__ == "__main__":
    # Default commit message to today's date
    commit_message = date.today().strftime("%Y-%m-%d")
    
    # Run the git commit and push process
    git_commit_and_push(commit_message)
