import random

class PersonalityModule:
    def __init__(self):
        # Placeholder personality settings.
        self.tone = "witty"  # Can be 'witty', 'formal', 'casual', etc.

    def get_response(self, input_text):
        """Generate a personality infused response."""
        responses = {
            "greeting": ["Hello, genius!", "Greetings, prodigy!", "Hi there, future Stark!"],
            "default": ["I'm on it!", "Right away!", "Consider it done!"]
        }
        # Simple rule: if greeting word is detected, respond with a greeting.
        if any(word in input_text.lower() for word in ["hi", "hello", "hey"]):
            response = random.choice(responses["greeting"])
        else:
            response = random.choice(responses["default"])
        print(f"[Personality] Responding with: {response}")
        return response 

    def process_interaction(self, input_text):
        """Compatibility wrapper for JarvisCore interactions."""
        if not input_text:
            return "I'm here whenever you need me, sir."
        return self.get_response(input_text)
