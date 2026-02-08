import speech_recognition as sr
import pyttsx3
import time

class VoiceInterface:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.recognizer = sr.Recognizer()
        self.use_microphone = False
        self.enabled = True
        
        # Try to initialize microphone, but don't fail if it's not available
        try:
            self.microphone = sr.Microphone()
            self.use_microphone = True
            print("[Voice] Microphone initialized successfully")
        except Exception as e:
            print(f"[Voice] Could not initialize microphone: {e}")
            print("[Voice] Using simulated voice input instead")

    def listen(self):
        """Listen to user input via microphone or simulate input."""
        if not self.enabled:
            return ""

        if self.use_microphone:
            try:
                with self.microphone as source:
                    print("[Voice] Listening...")
                    audio = self.recognizer.listen(source)
                try:
                    # Recognize speech using Google's API
                    command = self.recognizer.recognize_google(audio)
                    print(f"[Voice] Recognized: {command}")
                    return command.lower()
                except sr.UnknownValueError:
                    print("[Voice] Could not understand audio.")
                    return ""
                except sr.RequestError as e:
                    print(f"[Voice] Recognition error; {e}")
                    return ""
            except Exception as e:
                print(f"[Voice] Error during listening: {e}")
                return ""
        else:
            # Simulated input for testing
            print("[Voice] Simulated listening mode - type your command:")
            command = input("> ")
            return command.lower()

    def speak(self, text):
        """Speak the given text using text-to-speech engine."""
        print(f"[Jarvis Says] {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[Voice] Error during speech: {e}")
            # Fallback to just printing
            print(f"[Voice] Could not speak: {text}") 