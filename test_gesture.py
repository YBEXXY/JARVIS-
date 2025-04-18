#!/usr/bin/env python
"""
Gesture Recognition Test Script
-----------------------------
This script tests the gesture recognition module directly,
without running the entire Jarvis system.
"""

import sys
import time
from modules.gesture_recognition import GestureRecognition

def main():
    print("=" * 50)
    print("Gesture Recognition Test")
    print("=" * 50)
    print("This script will test the gesture recognition module directly.")
    print("A window titled 'Gesture Recognition' should open showing your camera feed.")
    print("Try making different gestures to see if they are detected.")
    print("Press 'q' in the gesture window to quit.")
    print("=" * 50)
    
    # Create gesture recognition instance
    gesture = GestureRecognition()
    
    # Start gesture recognition
    if not gesture.start():
        print("ERROR: Failed to start gesture recognition")
        return
    
    print("\nGesture recognition started successfully!")
    print("Available gestures and their actions:")
    print("  👋 Wave - Toggle voice recognition")
    print("  👍 Thumbs Up - Confirm/Accept")
    print("  👎 Thumbs Down - Cancel/Reject")
    print("  👆 Point - Select/Choose")
    print("  👉 Swipe Right - Next/Forward")
    print("  👈 Swipe Left - Previous/Back")
    print("  ✊ Fist - Stop/Pause")
    print("  ✋ Open Hand - Start/Resume")
    print("\nPress Ctrl+C to exit this script")
    
    try:
        # Keep the script running
        while True:
            # Get the latest gesture
            current_gesture = gesture.detect_gesture()
            
            # Print the gesture if it's not "none"
            if current_gesture != "none":
                print(f"Detected gesture: {current_gesture}")
            
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