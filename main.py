# main.py - The single entry point for automated execution

import requests
import json
from export_results import export_to_csv # Import the export function
from app import app # Import the Flask app object (if needed for context, though we use requests)
import subprocess
import time
import sys

FLASK_URL = "http://127.0.0.1:5000/generate-emails"

def run_automation_flow():
    """
    Executes the full workflow: 
    1. Generates CSV preview.
    2. Runs the live email sending logic by calling the Flask endpoint.
    """
    print("--- 1. Generating CSV Preview (pilot_output.csv) ---")
    export_to_csv()
    print("✅ CSV Export complete: pilot_output.csv")
    
    # --- 2. Run Live Email Sending Workflow ---
    print("\n--- 2. Starting Live Email Sending Workflow via Flask Endpoint ---")
    
    # Start the Flask app in the background using subprocess
    # Note: This is a robust way to chain web service execution in a script.
    print("Starting Flask server in background...")
    try:
        # Use sys.executable to ensure the current Python environment is used
        flask_process = subprocess.Popen([sys.executable, 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3) # Give Flask time to start up

        # Hit the endpoint to trigger the workflow
        print(f"Making GET request to {FLASK_URL}...")
        response = requests.get(FLASK_URL, timeout=300) # 5 min timeout for API calls

        # --- 3. Workflow Summary ---
        print("\n--- 3. Workflow Summary ---")
        if response.status_code == 200:
            results = response.json()
            for res in results:
                status = "✅ SENT" if res.get('sent') else f"❌ FAILED ({res.get('to')})"
                print(f"{status}: {res.get('subject')}")
        else:
            print(f"❌ Failed to trigger Flask endpoint. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.ConnectionError:
        print(f"🚨 Connection Error: Could not connect to {FLASK_URL}. Ensure Flask started correctly.")
    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")
    finally:
        # Crucially, terminate the background Flask process
        if 'flask_process' in locals() and flask_process.poll() is None:
            print("\nShutting down background Flask server...")
            flask_process.terminate()
            flask_process.wait(timeout=5)
            print("Server shut down.")

if __name__ == '__main__':
    run_automation_flow()