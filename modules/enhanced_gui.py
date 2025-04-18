import tkinter as tk
from tkinter import ttk
import threading
import queue
import math
import random
import time
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import io
import base64
import os

class EnhancedGUI:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.status_label = None
        self.output_text = None
        self.entry = None
        self.send_button = None
        self.command_queue = queue.Queue()
        self.gui_thread = None
        self.running = True
        
        # Animation variables
        self.sphere_radius = 100
        self.sphere_center = (300, 200)
        self.sphere_color = "#00FFFF"  # Default cyan
        self.pulse_radius = 0
        self.pulse_growing = True
        self.audio_levels = [0] * 50  # For audio visualization
        self.current_task = "Idle"
        self.task_status = "Ready"
        
        # Load sound effects
        self.startup_sound = self._load_sound("startup.wav")
        self.listening_sound = self._load_sound("listening.wav")
        self.thinking_sound = self._load_sound("thinking.wav")
        self.responding_sound = self._load_sound("responding.wav")
        
        # Animation thread
        self.animation_thread = None
        self.bg_image = None

    def _create_techy_background(self):
        """Create a techy background with grid lines and subtle effects."""
        width, height = 800, 600
        image = Image.new('RGBA', (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        
        # Draw grid lines
        for i in range(0, width, 50):
            draw.line([(i, 0), (i, height)], fill=(0, 50, 100, 50), width=1)
        for i in range(0, height, 50):
            draw.line([(0, i), (width, i)], fill=(0, 50, 100, 50), width=1)
            
        # Add some techy elements
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(5, 20)
            draw.ellipse([x, y, x+size, y+size], fill=(0, 100, 200, 30))
            
        return ImageTk.PhotoImage(image)
    
    def _load_sound(self, filename):
        """Load a sound file or return None if not found."""
        try:
            # Check if the file exists in the sounds directory
            sound_path = os.path.join("sounds", filename)
            if os.path.exists(sound_path):
                return sound_path
            return None
        except Exception as e:
            print(f"Error loading sound {filename}: {e}")
            return None
    
    def _play_sound(self, sound_file):
        """Play a sound file if available."""
        if sound_file and os.path.exists(sound_file):
            try:
                import winsound
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                print(f"Error playing sound: {e}")
    
    def create_widgets(self):
        """Create the enhanced GUI widgets."""
        # Set window properties
        self.root.title("JARVIS Interface")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas for sphere and animations
        self.canvas = tk.Canvas(main_frame, width=600, height=400, bg="#000000", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Set background image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        
        # Create status frame
        status_frame = tk.Frame(main_frame, bg="#000000")
        status_frame.pack(fill=tk.X, padx=20)
        
        # Task status
        self.task_label = tk.Label(status_frame, text="Current Task: Idle", 
                                  font=("Consolas", 12), fg="#00FFFF", bg="#000000")
        self.task_label.pack(side=tk.LEFT, padx=10)
        
        # Status indicator
        self.status_indicator = tk.Label(status_frame, text="●", 
                                        font=("Arial", 16), fg="#00FF00", bg="#000000")
        self.status_indicator.pack(side=tk.RIGHT, padx=10)
        
        # Create output text area with custom styling
        self.output_text = tk.Text(main_frame, height=8, width=70, 
                                  font=("Consolas", 10), bg="#001010", fg="#00FFFF",
                                  insertbackground="#00FFFF")
        self.output_text.pack(pady=10, padx=20, fill=tk.X)
        
        # Create input frame
        input_frame = tk.Frame(main_frame, bg="#000000")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Command entry
        self.entry = ttk.Entry(input_frame, width=60, font=("Consolas", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind Enter key to send command
        self.entry.bind("<Return>", lambda event: self.send_command())
        
        # Start animation
        self._start_animation()
        
        # Play startup sound
        self._play_sound(self.startup_sound)
        
        # Display welcome message
        self.display_output("JARVIS Online. All systems operational.")
        self.update_task("System Initialization", "Complete")

    def _start_animation(self):
        """Start the animation loop."""
        self._animate()
    
    def _animate(self):
        """Animate the sphere and audio visualization."""
        if not self.running or not self.canvas:
            return
            
        # Clear previous frame
        self.canvas.delete("sphere", "pulse", "audio")
        
        # Draw sphere
        x, y = self.sphere_center
        self.canvas.create_oval(x-self.sphere_radius, y-self.sphere_radius,
                               x+self.sphere_radius, y+self.sphere_radius,
                               fill=self.sphere_color, outline="#FFFFFF", width=2,
                               tags="sphere")
        
        # Draw pulse effect
        if self.pulse_growing:
            self.pulse_radius += 2
            if self.pulse_radius >= 20:
                self.pulse_growing = False
        else:
            self.pulse_radius -= 2
            if self.pulse_radius <= 0:
                self.pulse_growing = True
                
        self.canvas.create_oval(x-self.sphere_radius-self.pulse_radius, 
                               y-self.sphere_radius-self.pulse_radius,
                               x+self.sphere_radius+self.pulse_radius, 
                               y+self.sphere_radius+self.pulse_radius,
                               outline=self.sphere_color, width=1, tags="pulse")
        
        # Draw audio visualization
        bar_width = 8
        bar_spacing = 2
        bar_height_factor = 3
        start_x = 100
        start_y = 350
        
        for i, level in enumerate(self.audio_levels):
            bar_height = level * bar_height_factor
            x1 = start_x + i * (bar_width + bar_spacing)
            y1 = start_y - bar_height
            x2 = x1 + bar_width
            y2 = start_y
            
            # Color gradient based on height
            color = self._get_gradient_color(level, 0, 1)
            
            self.canvas.create_rectangle(x1, y1, x2, y2, 
                                        fill=color, outline="", tags="audio")
        
        # Update audio levels (simulate with random values for now)
        self.audio_levels = self.audio_levels[1:] + [random.random() * 0.5 + 0.5]
        
        # Schedule next animation frame
        self.root.after(50, self._animate)
    
    def _get_gradient_color(self, value, min_val, max_val):
        """Get a color from a gradient based on value."""
        # Normalize value
        norm = (value - min_val) / (max_val - min_val)
        
        # Create gradient from blue to cyan to white
        if norm < 0.5:
            # Blue to cyan
            r = 0
            g = int(255 * (norm * 2))
            b = 255
        else:
            # Cyan to white
            r = int(255 * ((norm - 0.5) * 2))
            g = 255
            b = 255
            
        return f"#{r:02x}{g:02x}{b:02x}"

    def update_status(self, msg):
        """Update status display in GUI."""
        if self.status_indicator:
            self.root.after(0, lambda: self.status_indicator.config(text="●"))
    
    def update_task(self, task, status):
        """Update the current task and status."""
        self.current_task = task
        self.task_status = status
        
        if self.task_label:
            self.root.after(0, lambda: self.task_label.config(
                text=f"Current Task: {task} - {status}"))
    
    def display_output(self, msg):
        """Display messages in the output text widget."""
        if self.output_text:
            self.root.after(0, lambda: self._append_to_output(msg))

    def _append_to_output(self, msg):
        """Thread-safe method to append text to output widget."""
        self.output_text.insert(tk.END, f"{msg}\n")
        self.output_text.see(tk.END)
        
        # Update audio visualization with a burst
        for i in range(10):
            if i < len(self.audio_levels):
                self.audio_levels[i] = 1.0

    def send_command(self):
        """Handle manual command from GUI entry."""
        if self.entry:
            cmd = self.entry.get()
            self.entry.delete(0, tk.END)
            self.display_output(f"You: {cmd}")
            
            # Change sphere color to indicate processing
            self.sphere_color = "#FF00FF"  # Magenta for processing
            self.update_task("Processing Command", "Active")
            
            # Add command to queue for processing
            self.command_queue.put(cmd)

    def process_commands(self):
        """Process commands from the queue."""
        try:
            while not self.command_queue.empty():
                cmd = self.command_queue.get_nowait()
                from jarvis_core import JarvisCore
                JarvisCore.process_command(cmd)
        except queue.Empty:
            pass
        except Exception as e:
            print(f"[GUI] Error processing command: {e}")
        
        # Schedule the next check
        if self.running and self.root:
            self.root.after(100, self.process_commands)

    def set_listening_mode(self, is_listening):
        """Set the GUI to listening mode."""
        if is_listening:
            self.sphere_color = "#FF0000"  # Red for listening
            self.update_task("Listening", "Active")
            self._play_sound(self.listening_sound)
        else:
            self.sphere_color = "#00FFFF"  # Cyan for idle
            self.update_task("Idle", "Ready")

    def set_responding_mode(self, is_responding):
        """Set the GUI to responding mode."""
        if is_responding:
            self.sphere_color = "#0000FF"  # Blue for responding
            self.update_task("Responding", "Active")
            self._play_sound(self.responding_sound)
        else:
            self.sphere_color = "#00FFFF"  # Cyan for idle
            self.update_task("Idle", "Ready")

    def _run_gui(self):
        """Run the GUI main loop."""
        if self.root:
            try:
                self.root.mainloop()
            except Exception as e:
                print(f"Error in GUI thread: {e}")
            finally:
                self.running = False

    def start(self):
        """Start the GUI in the main thread."""
        if not self.root:
            self.root = tk.Tk()
            self.bg_image = self._create_techy_background()
            self.create_widgets()
            self._start_animation()
            self._play_sound(self.startup_sound)
            self.display_output("JARVIS Online. All systems operational.")
            self.update_task("System Initialization", "Complete")

    def stop(self):
        """Stop the GUI."""
        self.running = False
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except Exception as e:
                print(f"Error stopping GUI: {e}")
            finally:
                self.root = None 