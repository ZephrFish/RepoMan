import os
import random
import subprocess
import requests
import ollama
import toml
import argparse
from datetime import datetime, timedelta

# Load configuration from vars.toml
config = toml.load("vars.toml")

# GitHub settings
GITHUB_USERNAME = config["GITHUB_USERNAME"]
GITHUB_TOKEN = config["GITHUB_TOKEN"]

# Git user details
git_user_name = config["GIT_USER_NAME"]
git_user_email = config["GIT_USER_EMAIL"]

# Ollama Model
OLLAMA_MODEL = config.get("OLLAMA_MODEL", "llama2")  # Default to llama2

# Function to generate a random date for backdated commits
def random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2025, 1, 1)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M:%S")

# 🔹 Function to Generate Repo Names Using Ollama
def generate_repo_name(verbose=False):
    """Use Ollama to generate a unique repository name and ensure it has no prefixes."""
    if verbose:
        print("🔹 Generating repository name using Ollama...")

    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": "You generate short, creative repository names. DO NOT use phrases like 'Sure!', 'Here is', or explanations. Return ONLY the repository name, without punctuation or markdown formatting."},
        {"role": "user", "content": "Generate a unique, short repository name (max 50 characters) for a software project."}
    ])

    # Extract raw response
    repo_name = response["message"]["content"].strip()

    # **Remove AI-generated prefixes**
    unwanted_phrases = [
        "Sure! ", "Here is a unique and short repository name:", 
        "Here is an example:", "Generated repository name:", 
        "Suggested name:", "A possible repository name:"
    ]
    for phrase in unwanted_phrases:
        if repo_name.startswith(phrase):
            repo_name = repo_name[len(phrase):].strip()

    # **Ensure name is within length limits**
    repo_name = repo_name[:50].replace(" ", "-")  # Truncate & replace spaces

    if verbose:
        print(f"✅ Repository name generated: {repo_name}")

    return repo_name

# 🔹 Function to Generate Repo Descriptions Using Ollama
def generate_repo_description(verbose=False):
    """Use Ollama to generate a dynamic repository description without quotation marks."""
    if verbose:
        print("🔹 Generating repository description using Ollama...")

    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": "You generate concise repository descriptions. DO NOT use quotation marks (\"), explanations, or markdown formatting. Return ONLY the raw description."},
        {"role": "user", "content": "Generate a short, professional description for a software project, avoiding quotation marks."}
    ])

    # Extract and clean response
    description = response["message"]["content"].strip()

    # **Remove unwanted characters**
    description = description.replace('"', '')  # Strip out all quotation marks

    if verbose:
        print(f"✅ Repository description generated: {description}")

    return description

# 🔹 Function to Generate AI-Powered Commit Messages
def generate_commit_message(verbose=False):
    """Use Ollama to generate a commit message with no extra explanations."""
    if verbose:
        print("🔹 Generating commit message using Ollama...")

    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": "You generate realistic commit messages. DO NOT provide explanations, introductions, or markdown formatting—return ONLY the commit message."},
        {"role": "user", "content": "Generate a short, professional commit message for software development."}
    ])

    # Extract and clean response
    commit_msg = response["message"]["content"].strip()

    # **Remove possible AI prefixes**
    unwanted_phrases = [
        "Sure! ", "Here's a commit message:", "Here's an example:", 
        "A possible commit message:", "Example:", "Generated commit message:"
    ]
    for phrase in unwanted_phrases:
        if commit_msg.startswith(phrase):
            commit_msg = commit_msg[len(phrase):].strip()

    if verbose:
        print(f"✅ Commit message generated: {commit_msg}")

    return commit_msg

# 🔹 Function to Create a GitHub Repository
def create_github_repo(repo_name, repo_description, verbose=False):
    if verbose:
        print(f"🚀 Creating GitHub repository: {repo_name}")
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {"name": repo_name, "private": False, "description": repo_description}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        if verbose:
            print(f"✅ Repository '{repo_name}' successfully created on GitHub.")
        return f"git@github.com:{GITHUB_USERNAME}/{repo_name}.git"
    else:
        print(f"❌ Failed to create repository {repo_name}: {response.json()}")
        return None

# 🔹 Function to Modify Files Using Ollama
def ask_ollama(file_content, verbose=False):
    """Send file content to Ollama and enforce strict output of only modified content."""
    if verbose:
        print("🤖 Sending file content to Ollama for modification...")

    response = ollama.chat(model=OLLAMA_MODEL, messages=[
        {"role": "system", "content": (
            "You are a highly skilled AI that modifies and refactors code. "
            "Your task is to update the provided code to add missing functionality "
            "or improve its structure. "
            "Return only the modified file content, with no explanations, no markdown, "
            "and no introductory or concluding remarks. "
            "Your response must be a valid file with all necessary content."
        )},
        {"role": "user", "content": file_content}
    ])

    # Extract response and ensure it's clean
    modified_content = response["message"]["content"].strip()

    # **Remove unwanted AI-generated prefixes**
    unwanted_phrases = [
        "Here is the modified version of the file:", 
        "Here is your updated code:", 
        "I've made some improvements:", 
        "Here is an optimized version:",
        "Updated version:",
        "Here's the complete file:"
    ]
    for phrase in unwanted_phrases:
        if modified_content.startswith(phrase):
            modified_content = modified_content[len(phrase):].strip()

    if verbose:
        print("✅ File successfully modified by Ollama.")

    return modified_content

# 🔹 Function to Modify a Random File in the Repository
def modify_all_files(repo, verbose=False):
    """Modify all files in the repository using Ollama."""
    file_paths = []
    
    for root, _, files in os.walk(repo):
        if ".git" in root.split
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    if not file_paths:
        if verbose:
            print(f"⚠️ No modifiable files in {repo}. Skipping modification.")
        return

    for file_to_modify in file_paths:
        with open(file_to_modify, "r", encoding="utf-8") as f:
            original_content = f.read()

        if verbose:
            print(f"🤖 Using Ollama to modify {file_to_modify}...")

        modified_content = ask_ollama(original_content, verbose)

        with open(file_to_modify, "w", encoding="utf-8") as f:
            f.write(modified_content)

        if verbose:
            print(f"✅ {file_to_modify} modified successfully.")

# 🔹 Function to Create, Commit, and Push Repositories
def setup_repository(verbose=False):
    """Create repository structure, files, and push to GitHub."""
    repo_name = generate_repo_name(verbose)
    repo_description = generate_repo_description(verbose)

    print(f"📁 Setting up repository: {repo_name} ({repo_description})")

    # **Ensure directories exist**
    os.makedirs(f"{repo_name}/scripts", exist_ok=True)
    os.makedirs(f"{repo_name}/config", exist_ok=True)
    os.makedirs(f"{repo_name}/docs", exist_ok=True)

    # **Git Setup**
    subprocess.run(["git", "init"], cwd=repo_name)
    subprocess.run(["git", "config", "user.name", git_user_name], cwd=repo_name)
    subprocess.run(["git", "config", "user.email", git_user_email], cwd=repo_name)

    # **README File**
    with open(f"{repo_name}/README.md", "w", encoding="utf-8") as f:
        f.write(f"# {repo_name}\n\n{repo_description}")

    # **.gitignore**
    with open(f"{repo_name}/.gitignore", "w", encoding="utf-8") as f:
        f.write("node_modules/\n.DS_Store\nvenv/\nlogs/\n")

    # **Scripts Directory - Add Sample Script**
    script_path = f"{repo_name}/scripts/script.py"
    if not os.path.exists(script_path):
       with open(script_path, "w", encoding="utf-8") as f:
           f.write(f"""# Sample Python script
def greet():
    print("Hello from {repo_name}! This script is part of a dynamically generated repository.")

if __name__ == "__main__":
    greet()
""")
    os.chmod(script_path, 0o755)  # Ensure script is executable

    # **Config Directory - Add JSON Settings**
    config_path = f"{repo_name}/config/settings.json"
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(f'{{ "app_name": "{repo_name}", "version": "1.0.0", "enabled": true }}')

    # **Docs Directory - Add Simple HTML File**
    docs_path = f"{repo_name}/docs/index.html"
    if not os.path.exists(docs_path):
        with open(docs_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head><title>{repo_name}</title></head>
<body><h1>Welcome to {repo_name}</h1></body>
</html>""")

    if verbose:
        print(f"✅ All necessary files created in {repo_name}")

    # **Generate Commits**
    num_commits = random.randint(5, 30)
    commit_dates = sorted([random_date() for _ in range(num_commits)])

    for i, commit_date in enumerate(commit_dates):
        commit_msg = generate_commit_message(verbose)
        modify_all_files(repo_name, verbose)

        print(f"📌 Commit {i+1}/{num_commits}: {commit_msg} on {commit_date}")
        subprocess.run(["git", "add", "."], cwd=repo_name)
        subprocess.run(["git", "commit", "-m", commit_msg], env={**os.environ, "GIT_AUTHOR_DATE": commit_date, "GIT_COMMITTER_DATE": commit_date}, cwd=repo_name)

    # **Push to GitHub**
    remote_url = create_github_repo(repo_name, repo_description, verbose)
    if remote_url:
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=repo_name)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_name)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=repo_name)
        print(f"🚀 Pushed '{repo_name}' to GitHub!")

# 🔹 Function to Rollback Commits
def rollback_commits(repo, verbose=False):
    print(f"🔄 Rolling back commits for {repo}")

    rollback_count = random.randint(5, 20)
    total_commits = int(subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True).stdout.strip())

    if total_commits < rollback_count:
        print(f"⚠️ Not enough commits to rollback in {repo}. Skipping...")
        return

    subprocess.run(["git", "reset", "--hard", f"HEAD~{rollback_count}"], cwd=repo)
    subprocess.run(["git", "push", "--force"], cwd=repo)
    print(f"✅ Rolled back {rollback_count} commits in {repo}")

# CLI options
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5, help="Number of repositories to create (default: 5)")
    parser.add_argument("--rollback", action="store_true", help="Rollback last commits randomly")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    for _ in range(args.count):
        setup_repository(args.verbose)

    print("🎉 All AI-generated repositories are now live on GitHub!")