import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DeepSeekAgent:
    def __init__(self):
        self.api_key = "sk-0aaf3ac7be3b45c680b60493b8066c8a"  # Use your own API key
        self.base_url = "https://api.deepseek.com/v1"  # Verify the actual API endpoint
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    def query(self, prompt, model="deepseek-chat", max_tokens=150):
        """Send a query to the DeepSeek API"""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error querying DeepSeek API: {e}")
            return None
        
# Example usage
if __name__ == "__main__":
    agent = DeepSeekAgent()
    response = agent.query("Explain quantum computing in simple terms")
    print(response)