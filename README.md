# Repoman

## Overview

Repoman is a command-line tool designed to automate the creation, modification, and management of Git repositories. I created it as I wanted to see how do-able it was to create legimate looking commit history but as you'll see with this repo(pay attention to the commit history and `unhinged.log`) it sort of went off the rails a little bit.

It facilitates the generation of repositories with structured content, commits with backdated timestamps, and AI-generated commit messages to simulate realistic development activity. The tool can also modify commit history and rollback changes, making it useful for research, testing, and controlled environments.

## Features

### Repository Creation
- Dynamically generates repository names and descriptions.
- Structures repositories with predefined directories such as `scripts`, `config`, and `docs`.
- Creates essential files including `README.md`, `.gitignore`, and sample scripts.

### AI-Driven Content Generation
- Uses Ollama to generate realistic commit messages relevant to software development and the content within the repo.
- Modifies repository files to improve formatting, readability, and structure.
- Ensures commit messages are concise and meaningful without unnecessary AI-generated prefixes.

### Commit Management
- Backdates commits randomly within a specified date range to create an aged repository history.
- Allows rollback of a specified number of commits to simulate version history changes.
- Ensures commit authorship details match predefined user configurations.

### GitHub Integration
- Optionally creates remote repositories on GitHub using API authentication.
- Pushes repositories with structured commit histories and backdated commits.
- Uses force-pushing for rollback operations when modifying commit history.

## Installation

### Prerequisites
- Python 3.7+
- Git installed on the system
- Ollama installed and configured
- A valid GitHub account (if pushing repositories remotely)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/ZephrFish/repoman.git
   cd repoman
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `vars.toml` configuration file:
  ```toml
GITHUB_USERNAME = "USERNAME" # Username for whatever account you're writing to
GITHUB_TOKEN = "CLASSIC GIT TOKEN" # Get git token from developer settings in github 
OLLAMA_MODEL = "llama2"  # Change to "llama2", "gemma", etc.
GIT_USER_NAME = "GIT NAME" # Username variable for git config
GIT_USER_EMAIL = "EMAIL" # email variable for git config
   ```

## Usage

### Create New Repositories
To generate a specified number of repositories with AI-enhanced content:
```bash
python repoman.py --count 5
```

### Modify Commit History
To update commit messages and structure using AI-generated improvements:
```bash
python repoman.py
```

### Rollback Commit History
To remove the last few commits from all repositories:
```bash
python repoman.py --rollback
```

### Enable Verbose Mode
For detailed logging and debugging output:
```bash
python repoman.py -v
```

## Example Workflow
1. Generate 5 repositories:
   ```bash
   python repoman.py --count 5
   ```
2. Modify commit history and content:
   ```bash
   python repoman.py
   ```
3. Review commits:
   ```bash
   git log --oneline --date=iso
   ```
4. Push changes manually (if needed):
   ```bash
   git push
   ```

## Some Potential Use Cases
- **Software Development Simulation**: Generate realistic repositories with structured commit histories.
- **CTF Challenges**: Create repositories containing hidden information or staged changes.
- **Security Research**: Test automated analysis tools on dynamic and structured repositories.

## Disclaimer
This tool is intended for educational and research purposes only. Use responsibly and ensure compliance with applicable guidelines and policies when modifying or pushing repositories.

