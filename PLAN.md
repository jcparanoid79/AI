# AI Coding Assistant Plan

**Project Goal:** Create a web-based AI assistant using Flask and the Google Gemini API to help with coding tasks (generation, debugging, explanation, refactoring, documentation).

**Plan:**

1.  **Setup & Configuration (Requires 'Code' Mode):**
    *   **Modify `.env`:** Add the line `GEMINI_API_KEY=YOUR_API_KEY_HERE` to the existing `.env` file. (User needs to do this or we switch mode).
    *   **Create Files:**
        *   `gemini_agent_app.py`: New Flask application file.
        *   `templates/gemini_agent.html`: New HTML file for the web interface.
        *   `static/gemini_styles.css`: New CSS file for styling (optional, could modify existing `styles.css`).
    *   **Install Dependencies:** Add `Flask`, `google-generativeai`, and `python-dotenv` to the project requirements (likely via `pip install` and potentially a `requirements.txt` file).
    *   **Basic Flask Setup:** Initialize the Flask app in `gemini_agent_app.py`, configure it to load the `GEMINI_API_KEY` from `.env`.

2.  **Backend Development (Flask - `gemini_agent_app.py`):**
    *   **API Route:** Create a route (e.g., `/api/assist`) that accepts POST requests.
    *   **Request Handling:** The route will expect JSON data containing the `action` (e.g., 'generate', 'debug', 'explain') and the `prompt` (user's text or code).
    *   **Gemini Integration:**
        *   Import and initialize the `google.generativeai` client using the API key.
        *   Construct specific prompts for the Gemini model based on the requested `action` and `prompt`. For example:
            *   *Generate:* "Generate Python code for: {prompt}"
            *   *Debug:* "Find and fix errors in the following code, and explain the fix:\n```\n{prompt}\n```"
            *   *Explain:* "Explain the following code:\n```\n{prompt}\n```"
            *   *Refactor:* "Suggest improvements or refactorings for the following code:\n```\n{prompt}\n```"
            *   *Document:* "Write documentation (e.g., docstrings, comments) for the following code:\n```\n{prompt}\n```"
        *   Send the constructed prompt to the Gemini API.
    *   **Response Handling:** Return the response from the Gemini API as JSON to the frontend. Include error handling for API issues.
    *   **Main Route:** Create a root route (`/`) that renders the `gemini_agent.html` template.

3.  **Frontend Development (HTML/CSS/JS - `templates/gemini_agent.html`, `static/gemini_styles.css`):**
    *   **UI Structure (`gemini_agent.html`):**
        *   Dropdown/Radio buttons to select the `action`.
        *   Text area for user `prompt` input.
        *   Submit button.
        *   A designated area (e.g., a `<pre>` or `<div>`) to display the AI's response.
    *   **Styling (`gemini_styles.css`):** Add basic CSS for layout and appearance.
    *   **JavaScript (Inline or separate `.js` file):**
        *   Add an event listener to the submit button.
        *   On submit:
            *   Prevent default form submission.
            *   Get the selected `action` and the `prompt` text.
            *   Send a `fetch` POST request to the `/api/assist` backend route with the action and prompt in the JSON body.
            *   Handle the JSON response from the backend.
            *   Display the AI's response in the designated display area.
            *   Include basic loading indicators and error display.

**Simplified Flow Diagram:**

```mermaid
graph TD
    subgraph Browser
        UI[gemini_agent.html] -- User Interaction --> JS{Frontend JS}
        JS -- Fetch POST /api/assist (action, prompt) --> Backend
        Backend -- JSON Response (result) --> JS
        JS -- Updates --> UI
    end

    subgraph Server (Flask: gemini_agent_app.py)
        Backend[API Route /api/assist] -- Loads Key --> Env[.env File]
        Backend -- Constructs Prompt --> Gemini[Gemini API Call]
        Gemini -- AI Response --> Backend
        Backend -- Renders Template --> Render[Route /]
        Render -- Serves --> UI
    end

    style Env fill:#f9f,stroke:#333,stroke-width:2px
    style Gemini fill:#ccf,stroke:#333,stroke-width:2px