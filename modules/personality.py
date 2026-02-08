"""Personality layer for response shaping."""

from __future__ import annotations

import random


class PersonalityModule:
    def __init__(self, tone: str = "witty") -> None:
        self.tone = tone

    def get_response(self, input_text: str) -> str:
        responses = {
            "greeting": ["Hello, genius!", "Greetings, prodigy!", "Hi there, future Stark!"],
            "default": ["I'm on it!", "Right away!", "Consider it done!"],
        }
        key = "greeting" if any(word in input_text.lower() for word in ("hi", "hello", "hey")) else "default"
        return random.choice(responses[key])

    def process_interaction(self, input_text: str) -> str:
        if not input_text:
            return "I'm here whenever you need me, sir."
        return self.get_response(input_text)
