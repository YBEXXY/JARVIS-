"""Language model router with provider fallback strategy."""

from __future__ import annotations

import logging
import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMSelector:
    def __init__(self, openai_api_key: str | None = None, huggingface_api_key: str | None = None) -> None:
        self.openai_api_key = openai_api_key if openai_api_key is not None else os.getenv("OPENAI_API_KEY", "")
        self.huggingface_api_key = (
            huggingface_api_key if huggingface_api_key is not None else os.getenv("HUGGINGFACE_API_KEY", "")
        )

        self.default_model = "openai"
        self.models = {
            "openai": {
                "name": "gpt-3.5-turbo",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.openai_api_key}",
                },
            },
            "huggingface": {
                "name": "gpt2",
                "endpoint": "https://api-inference.huggingface.co/models/gpt2",
                "headers": {"Authorization": f"Bearer {self.huggingface_api_key}"},
            },
        }

        self.fallback_responses = [
            "I'm having trouble connecting to my language models right now.",
            "I'm experiencing some technical difficulties with my language processing.",
            "I'm unable to access my knowledge base at the moment.",
            "My language models are temporarily unavailable.",
            "I'm having trouble processing that request right now.",
        ]

    def query_llm(self, query: str, model: str | None = None) -> str:
        if not query:
            return "I didn't receive a query to process."

        model_name = model if model in self.models else self.default_model
        try:
            if model_name == "openai":
                return self._query_openai(query)
            if model_name == "huggingface":
                return self._query_huggingface(query)
            return self._local_processing(query)
        except Exception as exc:  # defensive boundary for provider adapters
            logger.exception("LLM query failed for model=%s: %s", model_name, exc)
            return self._local_processing(query)

    def _query_openai(self, query: str) -> str:
        if not self.openai_api_key:
            return self._local_processing(query)

        payload = {
            "model": self.models["openai"]["name"],
            "messages": [
                {"role": "system", "content": "You are JARVIS, a helpful AI assistant."},
                {"role": "user", "content": query},
            ],
            "max_tokens": 150,
            "temperature": 0.7,
        }

        response = requests.post(
            self.models["openai"]["endpoint"],
            headers=self.models["openai"]["headers"],
            json=payload,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        logger.warning("OpenAI API error: %s", response.status_code)
        return self._local_processing(query)

    def _query_huggingface(self, query: str) -> str:
        if not self.huggingface_api_key:
            return self._local_processing(query)

        payload = {"inputs": query, "parameters": {"max_length": 100, "temperature": 0.7}}
        response = requests.post(
            self.models["huggingface"]["endpoint"],
            headers=self.models["huggingface"]["headers"],
            json=payload,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()[0]["generated_text"].strip()
        logger.warning("Hugging Face API error: %s", response.status_code)
        return self._local_processing(query)

    def _local_processing(self, query: str) -> str:
        query_lower = query.lower()
        if "what is" in query_lower or "who is" in query_lower:
            return "I'm processing your question. This would normally be handled by my language models."
        if "how to" in query_lower or "how do" in query_lower:
            return "I'm processing your instructions. This would normally be handled by my language models."
        if any(word in query_lower for word in ("open", "start", "launch")):
            return "I would open that for you. This would normally be handled by my system commands."
        if "turn on" in query_lower or "turn off" in query_lower:
            return "I would control that device for you. This would normally be handled by my device controller."
        return random.choice(self.fallback_responses)

    def get_available_models(self) -> list[str]:
        return list(self.models.keys())

    def set_default_model(self, model_name: str) -> bool:
        if model_name in self.models:
            self.default_model = model_name
            return True
        return False
