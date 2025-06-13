from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# --- 1. Configuration ---
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"
TEMPERATURE = 0.3
HIGHLIGHTER_STYLE = "monokai"

# --- 2. OpenAI Client ---
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

# --- 3. Flask App Setup ---
app = Flask(__name__)

# --- 4. Code Generation Function ---
def generate_code(prompt):
    """Generates Python code based on the given prompt.

    Args:
        prompt: The user's request for code generation.

    Returns:
        A string containing the highlighted Python code.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Generate functional Python code."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE
        )
        code = response.choices[0].message.content
        return highlight_code(code)  # Use helper function
    except Exception as e:
        print(f"Error generating code: {e}")  # Log the error
        return "<pre><code>Error generating code. Please check the server logs.</code></pre>" # Return a graceful error to the user.

def highlight_code(code):
    """Highlights Python code using Pygments."""
    return highlight(code, PythonLexer(), HtmlFormatter(style=HIGHLIGHTER_STYLE))


# --- 5. Flask Routes ---
@app.route("/")
def home():
    """Renders the home page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generates code based on the user's prompt and returns it as JSON."""
    try:
        prompt = request.json.get("prompt")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        highlighted_code = generate_code(prompt)
        return jsonify({"code": highlighted_code})

    except Exception as e:
        print(f"Error processing request: {e}") # Log the error
        return jsonify({"error": "An error occurred while processing your request."}), 500  # Return a 500 error with a user-friendly message


# --- 6. App Entry Point ---
if __name__ == "__main__":
    app.run(debug=True)

