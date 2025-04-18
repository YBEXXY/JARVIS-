#!/usr/bin/env python
"""
Custom Gesture Recognition Test
-----------------------------
This script allows you to test gesture recognition with custom actions.
You can define what happens when each gesture is detected.
"""

import sys
import time
import os
from modules.gesture_recognition import GestureRecognition

# Define custom actions for each gesture
GESTURE_ACTIONS = {
    "wave": "Toggle voice recognition",
    "thumbs_up": "Confirm/Accept",
    "thumbs_down": "Cancel/Reject",
    "point": "Select/Choose",
    "swipe_right": "Next/Forward",
    "swipe_left": "Previous/Back",
    "fist": "Stop/Pause",
    "open_hand": "Start/Resume"
}

# Custom action implementations
def toggle_voice_recognition():
    print("🔊 Voice recognition toggled")
    
def confirm_action():
    print("✅ Action confirmed")
    
def cancel_action():
    print("❌ Action cancelled")
    
def select_option():
    print("👆 Option selected")
    
def next_item():
    print("👉 Moving to next item")
    
def previous_item():
    print("👈 Moving to previous item")
    
def stop_action():
    print("⏹️ Action stopped")
    
def start_action():
    print("▶️ Action started")

# Map gestures to their action functions
ACTION_FUNCTIONS = {
    "wave": toggle_voice_recognition,
    "thumbs_up": confirm_action,
    "thumbs_down": cancel_action,
    "point": select_option,
    "swipe_right": next_item,
    "swipe_left": previous_item,
    "fist": stop_action,
    "open_hand": start_action
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the header information."""
    print("=" * 60)
    print("Custom Gesture Recognition Test".center(60))
    print("=" * 60)
    print("This script allows you to test gesture recognition with custom actions.")
    print("A window titled 'Gesture Recognition' should open showing your camera feed.")
    print("Try making different gestures to see if they are detected.")
    print("Press 'q' in the gesture window to quit.")
    print("=" * 60)
    
    print("\nAvailable gestures and their actions:")
    for gesture, action in GESTURE_ACTIONS.items():
        print(f"  {gesture}: {action}")
    print("\nPress Ctrl+C to exit this script")
    print("=" * 60)

def main():
    clear_screen()
    print_header()
    
    # Create gesture recognition instance
    gesture = GestureRecognition()
    
    # Start gesture recognition
    if not gesture.start():
        print("ERROR: Failed to start gesture recognition")
        return
    
    print("\nGesture recognition started successfully!")
    
    # Keep track of the last gesture to avoid repeating the same action
    last_gesture = "none"
    last_action_time = 0
    action_cooldown = 1.0  # seconds
    
    try:
        # Keep the script running
        while True:
            # Get the latest gesture
            current_gesture = gesture.detect_gesture()
            current_time = time.time()
            
            # Process the gesture if it's not "none" and not the same as the last one
            if (current_gesture != "none" and 
                current_gesture != last_gesture and 
                current_time - last_action_time > action_cooldown):
                
                print(f"\n🎯 Detected gesture: {current_gesture}")
                
                # Execute the corresponding action
                if current_gesture in ACTION_FUNCTIONS:
                    ACTION_FUNCTIONS[current_gesture]()
                
                # Update the last gesture and time
                last_gesture = current_gesture
                last_action_time = current_time
            
            # Sleep to reduce CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Release resources
        gesture.release()
        print("Gesture recognition stopped")

if __name__ == "__main__":
    main() 