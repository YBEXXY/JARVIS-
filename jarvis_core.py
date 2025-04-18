import threading
import time
import queue
import random
from modules.voice_interface import VoiceInterface
from modules.gesture_recognition import GestureRecognition
from modules.llm_selector import LLMSelector
from modules.enhanced_gui import EnhancedGUI
from modules.device_controller import DeviceController
from modules.personality import PersonalityModule
from modules.threat_analyzer import ThreatAnalyzer

class JarvisCore:
    # Class-level instances for global access
    voice = None
    gesture = None
    llm = None
    gui = None
    device_controller = None
    personality = None
    threat_analyzer = None
    
    # Command queue for processing
    command_queue = queue.Queue()
    
    # Control flags
    running = True
    listening = False
    responding = False
    processing_command = False
    
    # Task tracking
    current_task = "Initializing"
    task_status = "Starting"
    
    @classmethod
    def initialize(cls):
        """Initialize all JARVIS modules."""
        print("[Jarvis] Initializing modules...")
        
        # Initialize modules
        cls.voice = VoiceInterface()
        cls.gesture = GestureRecognition()
        cls.llm = LLMSelector()
        cls.device_controller = DeviceController()
        cls.personality = PersonalityModule()
        cls.threat_analyzer = ThreatAnalyzer()
        
        # Register a test device
        cls.device_controller.register_device("lights", interface="mock_interface")
        
        # Initialize GUI last (it will display the startup message)
        cls.gui = EnhancedGUI()
        
        print("[Jarvis] All modules initialized successfully")
        return cls

    @classmethod
    def process_command(cls, command):
        """Process incoming commands."""
        if not command:
            return
            
        print(f"⚙️ Processing your command...")
        
        # Handle exit commands
        if command.lower() in ["exit", "shutdown", "quit"]:
            print("🤖 JARVIS: Shutting down...")
            cls.shutdown()
            return
            
        # Handle LLM queries
        if command.startswith("llm:"):
            query = command[4:].strip()
            response = cls.llm.query_llm(query)
            print(f"🤖 JARVIS: {response}")
            return
            
        # Handle device control commands
        if command.startswith("device:"):
            device_cmd = command[7:].strip()
            response = cls.device_controller.process_command(device_cmd)
            print(f"🤖 JARVIS: {response}")
            return
            
        # Handle gesture commands
        if command.startswith("gesture:"):
            gesture = command[8:].strip()
            cls._handle_gesture(gesture)
            return
            
        # Handle threat analysis commands
        if command.startswith("threat:"):
            threat_cmd = command[7:].strip()
            response = cls.threat_analyzer.analyze_threat(threat_cmd)
            print(f"🤖 JARVIS: {response}")
            return
            
        # Handle personality interactions
        if command.startswith("personality:"):
            personality_cmd = command[12:].strip()
            response = cls.personality.process_interaction(personality_cmd)
            print(f"🤖 JARVIS: {response}")
            return
            
        # Default response for unrecognized commands
        print("🤖 JARVIS: I'm not sure how to help with that yet, sir. Would you like me to search the internet for information about it?")

    @classmethod
    def _handle_gesture(cls, gesture):
        """Handle gesture-based commands."""
        gesture_actions = {
            "wave": lambda: cls._toggle_voice_recognition(),
            "thumbs_up": lambda: cls._confirm_action(),
            "thumbs_down": lambda: cls._cancel_action(),
            "point": lambda: cls._select_option(),
            "swipe_right": lambda: cls._next_item(),
            "swipe_left": lambda: cls._previous_item(),
            "fist": lambda: cls._stop_action(),
            "open_hand": lambda: cls._start_action()
        }
        
        if gesture in gesture_actions:
            gesture_actions[gesture]()
        else:
            print(f"🤖 JARVIS: Unrecognized gesture: {gesture}")
            
    @classmethod
    def _toggle_voice_recognition(cls):
        """Toggle voice recognition on/off."""
        cls.voice.enabled = not cls.voice.enabled
        status = "enabled" if cls.voice.enabled else "disabled"
        print(f"🤖 JARVIS: Voice recognition {status}")
        
    @classmethod
    def _confirm_action(cls):
        """Confirm the current action."""
        print("🤖 JARVIS: Action confirmed")
        
    @classmethod
    def _cancel_action(cls):
        """Cancel the current action."""
        print("🤖 JARVIS: Action cancelled")
        
    @classmethod
    def _select_option(cls):
        """Select the current option."""
        print("🤖 JARVIS: Option selected")
        
    @classmethod
    def _next_item(cls):
        """Move to the next item."""
        print("🤖 JARVIS: Moving to next item")
        
    @classmethod
    def _previous_item(cls):
        """Move to the previous item."""
        print("🤖 JARVIS: Moving to previous item")
        
    @classmethod
    def _stop_action(cls):
        """Stop the current action."""
        print("🤖 JARVIS: Action stopped")
        
    @classmethod
    def _start_action(cls):
        """Start the current action."""
        print("🤖 JARVIS: Action started")

    @classmethod
    def run_voice_loop(cls):
        """Continuously listen and process voice commands."""
        while cls.running:
            if not cls.processing_command and not cls.responding:
                cls.listening = True
                cls.gui.set_listening_mode(True)
                cls.gui.update_task("Listening", "Active")
                
                cmd = cls.voice.listen()
                
                cls.listening = False
                cls.gui.set_listening_mode(False)
                
                if cmd:
                    cls.gui.display_output(f"You said: {cmd}")
                    cls.process_command(cmd)
                    
            time.sleep(0.1)  # Reduce CPU usage

    @classmethod
    def run_threat_monitor(cls):
        """Periodically run the threat analyzer."""
        while cls.running:
            if not cls.processing_command:
                threat_level = cls.threat_analyzer.analyze()
                
                # Only announce high threats
                if threat_level >= 7:
                    cls.gui.update_task("Threat Alert", "High")
                    alert = f"High threat detected! Level {threat_level}"
                    cls.gui.display_output(f"JARVIS: {alert}")
                    cls.voice.speak(alert)
                    
            time.sleep(5)  # Check every 5 seconds

    @classmethod
    def run_gesture_loop(cls):
        """Periodically check for gestures."""
        print("[Jarvis] Starting gesture recognition thread...")
        
        # Make sure gesture recognition is initialized
        if cls.gesture is None:
            print("[Jarvis] ERROR: Gesture recognition module not initialized")
            return
            
        # Start the gesture recognition
        if not cls.gesture.start():
            print("[Jarvis] ERROR: Failed to start gesture recognition")
            return
            
        print("[Jarvis] Gesture recognition started successfully")
        print("[Jarvis] A window titled 'Gesture Recognition' should open showing your camera feed")
        print("[Jarvis] If you don't see this window, check if it's minimized or behind other windows")
        
        while cls.running:
            try:
                # Get the latest gesture
                gesture = cls.gesture.detect_gesture()
                
                # Process the gesture if it's not "none"
                if gesture != "none":
                    print(f"[Jarvis] Detected gesture: {gesture}")
                    cls.process_command(f"gesture:{gesture}")
                
                # Sleep to reduce CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                print(f"[Jarvis] Error in gesture loop: {e}")
                time.sleep(0.1)
                
        # Release resources when done
        cls.gesture.release()
        print("[Jarvis] Gesture recognition stopped")

    @classmethod
    def start(cls):
        """Start all JARVIS modules concurrently."""
        print("[Jarvis] Starting up...")
        
        # Initialize all modules
        cls.initialize()
        
        # Start GUI
        cls.gui.start()
        
        # Give GUI time to initialize
        time.sleep(1)
        
        # Start voice command thread
        voice_thread = threading.Thread(target=cls.run_voice_loop, daemon=True)
        voice_thread.start()
        
        # Start threat monitoring thread
        threat_thread = threading.Thread(target=cls.run_threat_monitor, daemon=True)
        threat_thread.start()
        
        # Start gesture detection thread
        gesture_thread = threading.Thread(target=cls.run_gesture_loop, daemon=True)
        gesture_thread.start()
        
        # Main loop for additional tasks
        try:
            while cls.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            cls.shutdown()

    @classmethod
    def shutdown(cls):
        """Shutdown procedures for JARVIS."""
        print("[Jarvis] Initiating shutdown sequence...")
        cls.running = False
        
        # Release resources
        if cls.gesture:
            cls.gesture.release()
            
        # Stop GUI
        if cls.gui:
            cls.gui.stop()
            
        print("[Jarvis] Shutdown complete.")

if __name__ == "__main__":
    # Start the JARVIS system
    JarvisCore.start() 