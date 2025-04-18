import os
import datetime
import webbrowser
import psutil
import requests
from typing import Optional

def get_weather(city: str = "London") -> str:
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}"
    except:
        return "Sorry, I couldn't fetch the weather information."

def get_system_info() -> str:
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return f"System status: CPU usage is at {cpu}% and memory usage is at {memory}%"

def execute_command(command: str) -> str:
    command = command.lower()

    # Time related commands
    if "time" in command:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}"
    
    elif "date" in command:
        now = datetime.datetime.now()
        return f"Today's date is {now.strftime('%B %d, %Y')}"

    # Web related commands
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for you, sir."
    
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google, sir."
    
    elif "search" in command:
        search_term = command.replace("search", "").strip()
        if search_term:
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            return f"Searching for {search_term}"
        return "What would you like me to search for, sir?"

    # System related commands
    elif "system status" in command or "system info" in command:
        return get_system_info()
    
    elif "weather" in command:
        # Extract city name if provided, default to London
        city = "London"
        if "in" in command:
            city = command.split("in")[-1].strip()
        return get_weather(city)

    # Conversation commands
    elif "how are you" in command:
        return "I'm functioning at optimal levels, sir. How may I assist you today?"
    
    elif "thank you" in command:
        return "You're welcome, sir."
    
    elif "good morning" in command or "good afternoon" in command or "good evening" in command:
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning, sir."
        elif 12 <= hour < 17:
            return "Good afternoon, sir."
        else:
            return "Good evening, sir."

    elif "shutdown" in command:
        return "Initiating shutdown sequence. Goodbye, sir."

    else:
        return "I'm not sure how to help with that yet, sir. Would you like me to search the internet for information about it?"
