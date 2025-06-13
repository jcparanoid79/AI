## Python Code Snippet for Ollama Phi Model Interface
# This code provides a simple interface to interact with the Ollama Phi model using HTTP requests.

import requests
import json

class OllamaPhi:
    def __init__(self, model="phi", host="localhost", port=11434):
        """
        Initialize the Ollama Phi model interface.
        
        Args:
            model (str): Model name (default: "phi")
            host (str): Ollama server host (default: "localhost")
            port (int): Ollama server port (default: 11434)
        """
        self.model = model
        self.base_url = f"http://{host}:{port}"
        self.session = requests.Session()
        
    def generate(self, prompt, **kwargs):
        """
        Generate text from the Phi model.
        
        Args:
            prompt (str): Input prompt
            **kwargs: Additional generation parameters (e.g., temperature, max_tokens)
            
        Returns:
            str: Generated text
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return json.loads(response.text)["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error generating response: {e}")
            return None

    def chat(self, messages, **kwargs):
        """
        Chat with the Phi model using a message history.
        
        Args:
            messages (list): List of message dictionaries with "role" and "content"
            **kwargs: Additional generation parameters
            
        Returns:
            str: Model's response
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            **kwargs
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return json.loads(response.text)["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"Error in chat: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize the Phi model
    phi = OllamaPhi()
    
    # Simple generation example
    prompt = "Explain quantum computing in simple terms."
    response = phi.generate(prompt, temperature=0.7, max_tokens=150)
    print("Generated response:")
    print(response)
    print("\n" + "="*80 + "\n")
    
    # Chat example
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What is it known for?"}
    ]
    # Generate a chat response
    chat_response = phi.chat(messages, temperature=0.7, max_tokens=150)  # Removed extra dot
    print("Chat response:")
    print(chat_response)