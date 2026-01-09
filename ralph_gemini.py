import os
import sys
import json
import subprocess
import re
from datetime import datetime

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRD_FILE = os.path.join(SCRIPT_DIR, "prd.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "progress.txt")
PROMPT_FILE = os.path.join(SCRIPT_DIR, "prompt.md")

def read_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def write_file(path, content):
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created/Updated: {path}")

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {path}")

def parse_xml_response(response):
    """
    Parses the LLM response for control tags:
    <commit>...</commit>
    <complete>...</complete>
    
    File operations are handled natively by the agent in YOLO mode.
    """
    
    # Regex for commit presence (Hybrid approach)
    commit_pattern = re.compile(r'<commit>(.*?)</commit>', re.DOTALL)
    commit_match = commit_pattern.search(response)
    if commit_match:
        message = commit_match.group(1).strip()
        print(f"Committing changes: {message}")
        subprocess.run(["git", "add", "."], cwd=SCRIPT_DIR, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=SCRIPT_DIR, check=False)

    # Regex for completion
    complete_pattern = re.compile(r'<complete>(.*?)</complete>', re.DOTALL)
    if complete_pattern.search(response):
        return True

    return False

def main():
    print("--- Ralph Gemini Wrapper (YOLO Native Mode) ---")
    
    # Tiny Prompt to bootstrap
    meta_prompt = (
        "You are Ralph, an autonomous coding agent. "
        "Your instruction sets are in 'prompt.md'. "
        "Your project context is in 'prd.json' and 'progress.txt'. "
        "First, READ 'prompt.md'. "
        "Then READ 'prd.json' and 'progress.txt'. "
        "Then USE YOUR FILE TOOLS to execute the next task. "
        "Finally, output a <commit> tag to save your work."
    )

    print(f"Sending meta-prompt to Gemini... (Length: {len(meta_prompt)} chars)")
    
    try:
        # Use --yolo for auto-approval of file tools
        cmd_str = f'gemini chat "{meta_prompt}" --yolo --include-directories . --output-format text'
        
        result = subprocess.run(
            cmd_str,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            print(f"Gemini CLI Error: {result.stderr}")
            # If prompt fails (e.g. strict safety), we might need to handle it.
            # But in YOLO mode it should proceed.
            if "Error" in result.stderr:
                 print("Attempting to continue despite CLI error code...")

        response = result.stdout
        print("\n--- Gemini Response ---")
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-----------------------")

        # 4. Check for Completion Signal
        if "RALPH_COMPLETE" in response:
            print("Ralph indicates completion.")
            print("<promise>COMPLETE</promise>")
            
    except Exception as e:
        print(f"Wrapper Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
