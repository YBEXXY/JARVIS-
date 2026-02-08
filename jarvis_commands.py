"""Command routing for general-purpose JARVIS actions."""

from __future__ import annotations

import datetime
import os
import webbrowser
from typing import Callable

import psutil
import requests

OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITY = "London"


def get_weather(city: str = DEFAULT_CITY) -> str:
    """Return a short weather summary for the provided city."""
    api_key = os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return "Weather service is not configured. Please set OPENWEATHER_API_KEY."

    try:
        response = requests.get(
            OPENWEATHER_URL,
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {description}."
    except requests.RequestException:
        return "Sorry, I couldn't fetch the weather information right now."
    except (KeyError, IndexError, TypeError, ValueError):
        return "I received an unexpected weather response. Please try again."


def get_system_info() -> str:
    """Return a snapshot of CPU and memory utilization."""
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return f"System status: CPU usage is {cpu}% and memory usage is {memory}%."


def _extract_city(command: str) -> str:
    if " in " not in command:
        return DEFAULT_CITY
    return command.split(" in ", maxsplit=1)[1].strip() or DEFAULT_CITY


def execute_command(command: str) -> str:
    """Execute supported command intents from a normalized text command."""
    command = command.lower().strip()

    if not command:
        return "Please tell me what you'd like me to do."

    if "time" in command:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"

    if "date" in command:
        return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}"

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for you, sir."

    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google, sir."

    if command.startswith("search") or " search " in command:
        search_term = command.replace("search", "", 1).strip()
        if not search_term:
            return "What would you like me to search for, sir?"
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        return f"Searching for {search_term}."

    if "system status" in command or "system info" in command:
        return get_system_info()

    if "weather" in command:
        return get_weather(_extract_city(command))

    conversational_responses: dict[str, Callable[[], str]] = {
        "how are you": lambda: "I'm functioning at optimal levels, sir. How may I assist you today?",
        "thank you": lambda: "You're welcome, sir.",
        "shutdown": lambda: "Initiating shutdown sequence. Goodbye, sir.",
    }

    for trigger, response_factory in conversational_responses.items():
        if trigger in command:
            return response_factory()

    if any(phrase in command for phrase in ("good morning", "good afternoon", "good evening")):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning, sir."
        if 12 <= hour < 17:
            return "Good afternoon, sir."
        return "Good evening, sir."

    return (
        "I'm not sure how to help with that yet, sir. "
        "Would you like me to search the internet for information about it?"
    )
