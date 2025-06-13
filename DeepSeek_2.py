# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI  # Use the correct OpenAI SDK import

# Set the API key and base URL directly on the openai module
client = OpenAI(api_key="sk-0aaf3ac7be3b45c680b60493b8066c8a", base_url="https://api.deepseek.com")

def ask_deepseek(question, system_role):
    data = {
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": question}
        ],
        "model": "deepseek-chat",  # or "deepseek-v3" if available
    }

    try:
        # Use the OpenAI SDK's `openai.ChatCompletion.create` method
        response = client.chat.completions.create(
            model=data["model"],
            messages=data["messages"]
        )
        return response.choices[0].message.content  # Return the content of the first choice

    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

answer = ask_deepseek("Help me to create a Ai agent with DeepSeek", "You are a Python developer")
print(answer)