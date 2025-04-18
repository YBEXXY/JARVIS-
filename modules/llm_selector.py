import requests
import json
import time
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMSelector:
    def __init__(self):
        # API keys from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        
        # Default model settings
        self.default_model = "openai"
        self.models = {
            "openai": {
                "name": "gpt-3.5-turbo",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}"
                }
            },
            "huggingface": {
                "name": "gpt2",
                "endpoint": "https://api-inference.huggingface.co/models/gpt2",
                "headers": {
                    "Authorization": f"Bearer {self.huggingface_api_key}"
                }
            }
        }
        
        # Fallback responses for when APIs are unavailable
        self.fallback_responses = [
            "I'm having trouble connecting to my language models right now.",
            "I'm experiencing some technical difficulties with my language processing.",
            "I'm unable to access my knowledge base at the moment.",
            "My language models are temporarily unavailable.",
            "I'm having trouble processing that request right now."
        ]
        
        print("[LLM] Initialized with API-based language models")
    
    def query_llm(self, query, model=None):
        """Query the selected language model with the given query."""
        if not query:
            return "I didn't receive a query to process."
        
        # Use specified model or default
        model_name = model if model and model in self.models else self.default_model
        
        try:
            # Try to use the selected API
            if model_name == "openai":
                return self._query_openai(query)
            elif model_name == "huggingface":
                return self._query_huggingface(query)
            else:
                return self._local_processing(query)
        except Exception as e:
            print(f"[LLM] Error querying {model_name}: {e}")
            # Fall back to local processing
            return self._local_processing(query)
    
    def _query_openai(self, query):
        """Query the OpenAI API."""
        if not self.openai_api_key:
            print("[LLM] OpenAI API key not found")
            return self._local_processing(query)
        
        try:
            payload = {
                "model": self.models["openai"]["name"],
                "messages": [
                    {"role": "system", "content": "You are JARVIS, a helpful AI assistant."},
                    {"role": "user", "content": query}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.models["openai"]["endpoint"],
                headers=self.models["openai"]["headers"],
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(f"[LLM] OpenAI API error: {response.status_code}")
                return self._local_processing(query)
        except Exception as e:
            print(f"[LLM] Error with OpenAI API: {e}")
            return self._local_processing(query)
    
    def _query_huggingface(self, query):
        """Query the Hugging Face API."""
        if not self.huggingface_api_key:
            print("[LLM] Hugging Face API key not found")
            return self._local_processing(query)
        
        try:
            payload = {
                "inputs": query,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                self.models["huggingface"]["endpoint"],
                headers=self.models["huggingface"]["headers"],
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result[0]["generated_text"].strip()
            else:
                print(f"[LLM] Hugging Face API error: {response.status_code}")
                return self._local_processing(query)
        except Exception as e:
            print(f"[LLM] Error with Hugging Face API: {e}")
            return self._local_processing(query)
    
    def _local_processing(self, query):
        """Process the query locally using simple pattern matching."""
        try:
            # Simple pattern matching for common query types
            query_lower = query.lower()
            
            # Check for question types
            if "what is" in query_lower or "who is" in query_lower:
                # Extract the subject of the question
                parts = query_lower.split("what is" if "what is" in query_lower else "who is")
                if len(parts) > 1:
                    subject = parts[1].strip().split()[0]
                    return f"I'm processing a query about {subject}. This would normally be handled by my language models."
                return "I'm processing your question. This would normally be handled by my language models."
            
            elif "how to" in query_lower or "how do" in query_lower:
                # Extract the action from the question
                parts = query_lower.split("how to" if "how to" in query_lower else "how do")
                if len(parts) > 1:
                    action = parts[1].strip().split()[0]
                    return f"I'm processing instructions about how to {action}. This would normally be handled by my language models."
                return "I'm processing your instructions. This would normally be handled by my language models."
            
            # Check for commands
            elif "open" in query_lower or "start" in query_lower or "launch" in query_lower:
                # Extract the application or website
                for word in ["open", "start", "launch"]:
                    if word in query_lower:
                        parts = query_lower.split(word)
                        if len(parts) > 1:
                            app = parts[1].strip()
                            return f"I would open {app} for you. This would normally be handled by my system commands."
            
            # Check for device control
            elif "turn on" in query_lower or "turn off" in query_lower:
                # Extract the device
                for phrase in ["turn on", "turn off"]:
                    if phrase in query_lower:
                        parts = query_lower.split(phrase)
                        if len(parts) > 1:
                            device = parts[1].strip()
                            action = "on" if "turn on" in query_lower else "off"
                            return f"I would turn {device} {action}. This would normally be handled by my device controller."
            
            # Default response
            return "I'm processing your request. This would normally be handled by my language models."
        except Exception as e:
            print(f"[LLM] Error in local processing: {e}")
            return random.choice(self.fallback_responses)
    
    def get_available_models(self):
        """Get a list of available models."""
        return list(self.models.keys())
    
    def set_default_model(self, model_name):
        """Set the default model to use."""
        if model_name in self.models:
            self.default_model = model_name
            return True
        return False 