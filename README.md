# Code Sentry

Code Sentry is an AI-powered security code reviewer that utilizes the Google Gen AI SDK to analyze Python code snippets for potential vulnerabilities. It combines a local heuristic-based scanner (`scan_vulnerabilities`) with the analytical capabilities of the Gemini model to provide structured, conversational security feedback to developers.

## Prerequisites

- Python 3.10+
- A valid Gemini API Key

## Setup Instructions

1. Ensure you have the required dependencies installed:
   ```bash
   pip install google-genai
   ```

2. Export your Gemini API key as an environment variable:
   - **Windows (PowerShell):**
     ```powershell
     $env:GEMINI_API_KEY="your_api_key_here"
     ```
   - **Linux/macOS:**
     ```bash
     export GEMINI_API_KEY="your_api_key_here"
     ```

## How to Run

To run the built-in demo, simply execute the `main.py` file:

```bash
python main.py
```

### Running Tests
The project includes unit tests for the local `scan_vulnerabilities` tool. To run them:

```bash
python -m unittest tests/test_tools.py
```

## Example Input / Output

**Input Query:**
`Is this code safe for production use?`

**Input Code Snippet:**
```python
import os
import subprocess
import hashlib

def run_user_command(user_input):
    # Vulnerable to command injection
    subprocess.run("echo " + user_input, shell=True)
    
def hash_password(password):
    # Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()
```

**Expected AI Output:**
```
Summary Verdict: High Risk

Findings:
*   Severity: High, Line 7 - Insecure Subprocess detected. 
    Suggested Fix: Avoid using `shell=True` with user input to prevent command injection. Use a list of arguments instead: `subprocess.run(["echo", user_input])`.
*   Severity: Medium, Line 11 - Weak Hashing detected.
    Suggested Fix: `hashlib.md5` is considered cryptographically weak. Use a stronger algorithm like SHA-256 (`hashlib.sha256`) or, even better, a dedicated password hashing algorithm like Argon2 or bcrypt.

Explanation:
The provided code snippet has a couple of significant security concerns. First, running a subprocess with `shell=True` while incorporating user input directly opens the door to command injection. An attacker could provide input that executes arbitrary commands on your system. Second, using MD5 for hashing passwords is no longer recommended because it's fast and vulnerable to brute-force and collision attacks, making it easier for attackers to crack passwords. 
```

## Assumptions Made
- The new `google-genai` SDK is used, which automatically handles the execution and integration of tool calls (`tools=[scan_vulnerabilities]`).
- The application focuses on detecting vulnerabilities primarily through a heuristic/regex-based local tool, and depends on Gemini to structure the response and suggest fixes.
- Output formatting relies on Gemini's instruction-following capabilities guided by a detailed system prompt.
