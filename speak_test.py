from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Set up ElevenLabs client
client = ElevenLabs(
    api_key="sk_536823ef17fd7b4c2630a3ea55941b835d37342027adb3aa"  # Replace with your real key
)

# Generate speech
audio = client.generate(
    text="System reboot complete. Hello Commander, I am online.",
    voice="Rachel",  # Try voices like "Bella", "Antoni", etc.
    model="eleven_monolingual_v1"
)

# Play it
play(audio)
