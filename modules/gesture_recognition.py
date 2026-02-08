import cv2
import time
import threading
import queue
import numpy as np
import sys

class GestureRecognition:
    def __init__(self):
        self.running = False
        self.gesture_thread = None
        self.gesture_queue = queue.Queue()
        self.current_gesture = "none"
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # seconds
        self.debug_mode = True  # Enable debug mode
        self.camera_available = False
        
        # Initialize webcam
        print("[Gesture] Attempting to open camera...")
        self.cap = cv2.VideoCapture(0)
        
        # Try different camera indices if the first one fails
        if not self.cap.isOpened():
            print("[Gesture] Camera index 0 failed, trying index 1...")
            self.cap = cv2.VideoCapture(1)
            
        if not self.cap.isOpened():
            print("[Gesture] Camera index 1 failed, trying index 2...")
            self.cap = cv2.VideoCapture(2)
            
        if not self.cap.isOpened():
            print("[Gesture] ERROR: Could not open any camera. Please check your camera connection.")
            print("[Gesture] Available camera indices: 0, 1, 2")
            print("[Gesture] If you have an external camera, try connecting it and restarting.")
            return
            
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Test if we can actually read from the camera
        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("[Gesture] ERROR: Camera opened but cannot read frames.")
            print("[Gesture] This might be due to permission issues or the camera being used by another application.")
            return
            
        print(f"[Gesture] Camera successfully opened. Resolution: {frame.shape[1]}x{frame.shape[0]}")
        self.camera_available = True
        
        # Initialize background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, detectShadows=False)
        
        print("[Gesture] Initialized with basic gesture detection")
        print("[Gesture] Available gestures and their actions:")
        print("  👋 Wave - Toggle voice recognition")
        print("  👍 Thumbs Up - Confirm/Accept")
        print("  👎 Thumbs Down - Cancel/Reject")
        print("  👆 Point - Select/Choose")
        print("  👉 Swipe Right - Next/Forward")
        print("  👈 Swipe Left - Previous/Back")
        print("  ✊ Fist - Stop/Pause")
        print("  ✋ Open Hand - Start/Resume")
        print("\n[Gesture] IMPORTANT: A window titled 'Gesture Recognition' will open.")
        print("[Gesture] If you don't see this window, check if it's minimized or behind other windows.")
        print("[Gesture] Press 'q' in the gesture window to close it.")
    
    def start(self):
        """Start the gesture recognition system."""
        if self.running:
            return True

        if not self.camera_available or self.cap is None or not self.cap.isOpened():
            print("[Gesture] Cannot start gesture recognition: camera is unavailable")
            return False

        try:
            self.running = True
            self.gesture_thread = threading.Thread(target=self._gesture_loop)
            self.gesture_thread.daemon = True
            self.gesture_thread.start()
            
            print("[Gesture] Started basic gesture recognition")
            print("[Gesture] Press 'q' to quit the gesture window")
            return True
        except Exception as e:
            print(f"[Gesture] Error starting gesture recognition: {e}")
            return False
    
    def _gesture_loop(self):
        """Basic gesture recognition loop using OpenCV."""
        frame_count = 0
        last_fps_time = time.time()
        fps = 0
        
        while self.running:
            try:
                success, image = self.cap.read()
                if not success:
                    print("[Gesture] Failed to read frame from camera")
                    time.sleep(0.1)
                    continue
                
                # Calculate FPS
                frame_count += 1
                if time.time() - last_fps_time > 1.0:
                    fps = frame_count
                    frame_count = 0
                    last_fps_time = time.time()
                
                # Flip the image horizontally for a later selfie-view display
                image = cv2.flip(image, 1)
                
                # Create a copy for display
                display_image = image.copy()
                
                # Apply background subtraction
                fg_mask = self.bg_subtractor.apply(image)
                
                # Apply threshold to get binary image
                _, thresh = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
                
                # Find contours
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                if contours:
                    # Get the largest contour
                    largest_contour = max(contours, key=cv2.contourArea)
                    
                    # Draw the contour
                    cv2.drawContours(display_image, [largest_contour], -1, (0, 255, 0), 2)
                    
                    # Get the bounding rectangle
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cv2.rectangle(display_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    
                    # Calculate aspect ratio
                    aspect_ratio = float(w)/h
                    
                    # Detect gesture based on shape and aspect ratio
                    gesture = self._detect_gesture_type(largest_contour, aspect_ratio)
                    
                    current_time = time.time()
                    if gesture != "none" and (current_time - self.last_gesture_time) > self.gesture_cooldown:
                        self.current_gesture = gesture
                        self.last_gesture_time = current_time
                        self.gesture_queue.put(gesture)
                        print(f"[Gesture] Detected gesture: {gesture}")
                        
                        # Add visual feedback for the detected gesture
                        cv2.putText(display_image, f"Gesture: {gesture}", (10, 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Add debug information
                if self.debug_mode:
                    # Add FPS counter
                    cv2.putText(display_image, f"FPS: {fps}", (10, 60),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    
                    # Add gesture legend
                    cv2.putText(display_image, "Press 'q' to quit", (10, display_image.shape[0] - 20),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Add gesture instructions
                    cv2.putText(display_image, "Wave hand for 'wave'", (10, display_image.shape[0] - 50),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Display the image
                cv2.imshow('Gesture Recognition', display_image)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[Gesture] Quit command received, closing gesture window")
                    break
                
                # Add a small delay to reduce CPU usage
                time.sleep(0.01)
                
            except Exception as e:
                print(f"[Gesture] Error in gesture loop: {e}")
                time.sleep(0.1)
    
    def _detect_gesture_type(self, contour, aspect_ratio):
        """Detect the type of gesture based on contour shape and aspect ratio."""
        # Calculate area and perimeter
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # Calculate circularity
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Debug information
        if self.debug_mode and area > 100:  # Only for significant contours
            print(f"[Gesture Debug] Area: {area:.0f}, Circularity: {circularity:.2f}, Aspect Ratio: {aspect_ratio:.2f}")
        
        # Ignore very small or very large areas
        if area < 500 or area > 30000:
            return "none"
        
        # Detect wave (circular motion)
        if 0.6 < circularity < 0.9 and 0.8 < aspect_ratio < 1.2:
            return "wave"
        
        # Detect thumbs up (vertical rectangle)
        if aspect_ratio < 0.7 and area > 5000:
            return "thumbs_up"
        
        # Detect thumbs down (vertical rectangle)
        if aspect_ratio > 1.8 and area > 5000:
            return "thumbs_down"
        
        # Detect point (small area with high aspect ratio)
        if area < 3000 and (aspect_ratio > 1.5 or aspect_ratio < 0.5):
            return "point"
        
        # Detect swipe right (horizontal rectangle)
        if 1.5 < aspect_ratio < 3.0 and area > 3000:
            return "swipe_right"
        
        # Detect swipe left (horizontal rectangle)
        if 1.5 < aspect_ratio < 3.0 and area > 3000:
            return "swipe_left"
        
        # Detect fist (circular)
        if circularity > 0.8 and 0.8 < aspect_ratio < 1.2:
            return "fist"
        
        # Detect open hand (large area with medium aspect ratio)
        if area > 8000 and 0.5 < aspect_ratio < 1.5:
            return "open_hand"
        
        return "none"
    
    def detect_gesture(self):
        """Get the most recently detected gesture."""
        try:
            # Get the latest gesture from the queue
            while not self.gesture_queue.empty():
                self.current_gesture = self.gesture_queue.get_nowait()
            
            return self.current_gesture
        except queue.Empty:
            return "none"
    
    def release(self):
        """Release resources."""
        self.running = False
        if self.gesture_thread:
            self.gesture_thread.join(timeout=1.0)
        
        # Release the webcam and close windows
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        
        print("[Gesture] Released resources") 