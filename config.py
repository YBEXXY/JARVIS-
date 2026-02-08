"""Centralized runtime configuration for JARVIS."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # optional in minimal environments
    load_dotenv = lambda: None

load_dotenv()


@dataclass(frozen=True)
class JarvisConfig:
    """Configuration surface for runtime and integrations."""

    openai_api_key: str
    huggingface_api_key: str
    openweather_api_key: str
    threat_poll_interval_seconds: float = 5.0
    voice_poll_interval_seconds: float = 0.1
    gesture_poll_interval_seconds: float = 0.1

    @classmethod
    def from_env(cls) -> "JarvisConfig":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY", ""),
            openweather_api_key=os.getenv("OPENWEATHER_API_KEY", ""),
            threat_poll_interval_seconds=float(os.getenv("JARVIS_THREAT_INTERVAL", "5.0")),
            voice_poll_interval_seconds=float(os.getenv("JARVIS_VOICE_INTERVAL", "0.1")),
            gesture_poll_interval_seconds=float(os.getenv("JARVIS_GESTURE_INTERVAL", "0.1")),
        )
