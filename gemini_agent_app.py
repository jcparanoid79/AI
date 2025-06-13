import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=gemini_api_key)
    print("Gemini API Key loaded successfully.") # Add print statement for confirmation
except ValueError as e:
    print(f"Error: {e}")
    # Handle the error appropriately, maybe exit or provide a default behavior
    # For now, we'll just print the error and continue, but the API calls will fail.
except Exception as e:
    print(f"An unexpected error occurred during Gemini configuration: {e}")

# Initialize Flask app
app = Flask(__name__)

# --- Routes will be added here later ---

# Placeholder for the main route
@app.route('/')
def index():
    # Render the main HTML page
    return render_template('gemini_agent.html')

# Placeholder for the API route
@app.route('/api/assist', methods=['POST'])
def assist():
    # Handle requests from the frontend
    try:
        data = request.get_json()
        if not data or 'action' not in data or 'prompt' not in data:
            return jsonify({"error": "Missing 'action' or 'prompt' in request"}), 400

        action = data['action']
        user_prompt = data['prompt']

        # --- Construct prompt for Gemini based on action ---
        # (Using gemini-pro model, adjust if needed)
        model = genai.GenerativeModel('gemini-2.0-flash')

        system_prompts = {
            "generate": "Generate the following code based on the description:",
            "debug": "Find and fix errors in the following code, and explain the fix:",
            "explain": "Explain the following code:",
            "refactor": "Suggest improvements or refactorings for the following code:",
            "document": "Write documentation (e.g., docstrings, comments) for the following code:"
        }

        if action not in system_prompts:
            return jsonify({"error": "Invalid action specified"}), 400

        full_prompt = f"{system_prompts[action]}\n\n```\n{user_prompt}\n```"

        # --- Call Gemini API ---
        response = model.generate_content(full_prompt)

        # --- Return response ---
        # Accessing the text part of the response
        # Note: Error handling for blocked prompts or other API issues might be needed
        if response.parts:
             result_text = ''.join(part.text for part in response.parts)
        else:
             # Handle cases where the response might be empty or blocked
             # Check response.prompt_feedback for block reasons
             block_reason = response.prompt_feedback.block_reason if response.prompt_feedback else 'Unknown'
             result_text = f"Error: Response was empty or blocked. Reason: {block_reason}"
             # Consider returning an error status code as well
             # return jsonify({"error": result_text}), 500 # Example

        return jsonify({"result": result_text})

    except Exception as e:
        print(f"Error during API call: {e}")
        # Log the exception e for more details
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Runs the Flask app
    # Debug=True allows for auto-reloading and detailed error pages during development
    app.run(debug=True)