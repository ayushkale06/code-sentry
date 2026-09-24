import os
import sys
from google import genai
from google.genai import types

from tools import scan_vulnerabilities
from prompts import SYSTEM_PROMPT

def run_code_sentry(query: str, code_snippet: str):
    """
    Initializes the Gemini client, configures the system prompt and tools,
    and runs the code sentry agent on the provided query and snippet.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    # Using gemini-3.5-flash which is available in the API list
    model_id = 'gemini-3.5-flash'
    
    print("Code Sentry: Analyzing your code...\n" + "-"*40)
    
    prompt = f"User Query: {query}\n\nCode Snippet:\n```\n{code_snippet}\n```"
    
    import time
    try:
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # SDK recommends using Chat API for automatic function calling (AFC)
                chat = client.chats.create(
                    model=model_id,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        tools=[scan_vulnerabilities], # SDK automatically handles tool execution
                        temperature=0.2,
                    )
                )
                response = chat.send_message(prompt)
                print(response.text)
                break # Success, exit retry loop
            except Exception as e:
                if "503" in str(e) and attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"API is currently overloaded (503 UNAVAILABLE). Retrying in {wait} seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(wait)
                else:
                    print(f"Error during analysis: {e}")
                    break
    except Exception as e:
        print(f"Fatal error during setup: {e}")

if __name__ == "__main__":
    # Demo code with a clear vulnerability
    demo_code = '''
import os
import subprocess
import hashlib

def run_user_command(user_input):
    # Vulnerable to command injection
    subprocess.run("echo " + user_input, shell=True)
    
def hash_password(password):
    # Weak hashing algorithm
    return hashlib.md5(password.encode()).hexdigest()
'''
    demo_query = "Is this code safe for production use?"
    
    run_code_sentry(demo_query, demo_code)
