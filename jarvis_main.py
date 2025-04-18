import win32com.client
import speech_recognition as sr
import time
from jarvis_commands import execute_command
import os
from dotenv import load_dotenv
import threading
import queue
import random
import ctypes
from ctypes import wintypes
import win32api
import win32con
from modules.enhanced_gui import EnhancedGUI
import pyttsx3

# Load environment variables
load_dotenv()

# Initialize GUI
gui = EnhancedGUI()

# Initialize text-to-speech engine
try:
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 150)  # Speed of speech
    speaker.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
except Exception as e:
    print(f"Error initializing speech engine: {e}")
    speaker = None

# Global variables
listening_active = True
conversation_active = False
is_speaking = False
security_activated = False

# Queue for commands to process
command_queue = queue.Queue()

# Event to signal when to stop speaking
stop_speaking_event = threading.Event()

# Security settings
SECURITY_KEYWORD = "WAKE UP JARVIS"  # The keyword required to activate JARVIS

# Greeting responses for more natural conversation
greetings = [
    "Yes, sir. How may I assist you?",
    "I'm here, sir. What can I do for you?",
    "At your service, sir.",
    "How can I help you today, sir?",
    "I'm listening, sir."
]

# Interruption responses
interruption_responses = [
    "Yes, sir?",
    "I'm listening, sir.",
    "How can I help, sir?",
    "What can I do for you, sir?"
]

# Security responses
security_responses = {
    "success": [
        "Security clearance granted. Welcome, sir.",
        "Access authorized. How may I assist you, sir?",
        "Security protocol satisfied. At your service, sir."
    ],
    "failure": [
        "Access denied. Security protocol not satisfied.",
        "Unauthorized access attempt detected.",
        "Security clearance required for operation."
    ]
}

def speak(text):
    global is_speaking
    try:
        print("🤖 JARVIS:", text)
        if gui and gui.root:
            gui.root.after(0, lambda: gui.display_output(f"JARVIS: {text}"))
        is_speaking = True
        stop_speaking_event.clear()
        
        if speaker:
            speaker.say(text)
            speaker.runAndWait()
        
    except Exception as e:
        print(f"Error in speech generation: {e}")
    finally:
        is_speaking = False

def stop_speaking():
    """Stop the current speech"""
    global is_speaking
    if is_speaking and speaker:
        try:
            speaker.stop()
            is_speaking = False
            return True
        except Exception as e:
            print(f"Error stopping speech: {e}")
    return False

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 250  # Even lower threshold for better sensitivity
    recognizer.pause_threshold = 0.5  # Shorter pause threshold for faster response
    
    with sr.Microphone() as source:
        # Quick ambient noise adjustment
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            # Shorter timeout and phrase time limit for faster response
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            print("Processing speech...")
            
            try:
                text = recognizer.recognize_google(audio)
                print("🧠 You said:", text)
                
                # If JARVIS is speaking and we detect speech, interrupt him
                if is_speaking:
                    stop_speaking()
                    # Add a brief pause to acknowledge the interruption
                    time.sleep(0.5)
                    speak(random.choice(interruption_responses))
                
                return text.lower()
            except sr.UnknownValueError:
                # Don't print error to keep interface clean
                pass
            except sr.RequestError as e:
                print("⚠️ Could not request results; {0}".format(e))
                
        except sr.WaitTimeoutError:
            # Don't print timeout message to keep the interface clean
            pass
    
    return ""

def is_wake_word(command):
    wake_words = ["hey jarvis", "hello jarvis", "jarvis", "hey j", "hello j"]
    return any(wake_word in command for wake_word in wake_words)

def check_security_keyword(command):
    """Check if the security keyword is in the command"""
    global security_activated
    # Convert both to lowercase for case-insensitive comparison
    command_lower = command.lower()
    keyword_lower = SECURITY_KEYWORD.lower()
    
    # Check if the keyword is in the command
    if keyword_lower in command_lower:
        security_activated = True
        speak(random.choice(security_responses["success"]))
        return True
    return False

def continuous_listening():
    """Function to continuously listen in the background"""
    while listening_active:
        command = listen()
        if command:
            # Add command to queue for processing
            command_queue.put(command)

def process_command(command):
    """Process the command and respond"""
    global conversation_active, security_activated, listening_active
    
    if "exit" in command or "shutdown" in command:
        speak("Initiating shutdown sequence. Goodbye, sir.")
        listening_active = False
        return
    
    # Check for security keyword if not already activated
    if not security_activated:
        if check_security_keyword(command):
            return
        else:
            # If security is not activated and no keyword detected, reject access
            speak(random.choice(security_responses["failure"]))
            return
        
    # Check for wake word
    if is_wake_word(command):
        conversation_active = True
        speak(random.choice(greetings))
        return
        
    # Process command
    if command.strip() != "":
        print("⚙️ Processing your command...")
        response = execute_command(command)
        speak(response)
        
        # Check for follow-up indicators
        if "thank you" in command or "thanks" in command:
            speak("You're welcome, sir.")
        elif "goodbye" in command or "bye" in command:
            conversation_active = False
            speak("Goodbye, sir. Call me when you need me.")

def command_processor():
    """Process commands from the queue"""
    while listening_active:
        try:
            # Get command from queue with timeout
            command = command_queue.get(timeout=0.1)
            process_command(command)
        except queue.Empty:
            # No commands in queue, continue
            pass
        except Exception as e:
            print(f"Error processing command: {e}")

def main():
    global listening_active
    
    print("🤖 JARVIS is initializing...")
    
    # Start the GUI in the main thread
    gui.start()
    
    speak("JARVIS online. Security protocol active. Awaiting authorization.")
    print("\nTip: Say 'WAKE UP JARVIS' to activate JARVIS")
    print("     Say 'hey jarvis' or 'hello jarvis' after activation")
    print("     Say 'exit' or 'shutdown' to quit")
    print("     You can interrupt JARVIS while he's speaking by just talking")
    print(f"     Security keyword: '{SECURITY_KEYWORD}'")
    
    # Start continuous listening in a separate thread
    listen_thread = threading.Thread(target=continuous_listening)
    listen_thread.daemon = True
    listen_thread.start()
    
    # Start command processor in a separate thread
    processor_thread = threading.Thread(target=command_processor)
    processor_thread.daemon = True
    processor_thread.start()
    
    # Run the GUI main loop
    try:
        gui._run_gui()
    except KeyboardInterrupt:
        print("\nShutting down JARVIS...")
    finally:
        listening_active = False
        gui.stop()

if __name__ == "__main__":
    main()
