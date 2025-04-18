import tkinter as tk
from tkinter import ttk
import threading
import queue

class GUIHandler:
    def __init__(self):
        self.root = None
        self.status_label = None
        self.output_text = None
        self.entry = None
        self.send_button = None
        self.command_queue = queue.Queue()
        self.gui_thread = None
        self.running = True

    def create_widgets(self):
        # Minimalistic GUI design with a text area to display status.
        self.status_label = ttk.Label(self.root, text="Jarvis is operational.", font=("Helvetica", 14))
        self.status_label.pack(pady=10)
        self.output_text = tk.Text(self.root, height=15, width=60)
        self.output_text.pack(pady=10)
        self.entry = ttk.Entry(self.root, width=50)
        self.entry.pack(pady=5)
        self.send_button = ttk.Button(self.root, text="Send Command", command=self.send_command)
        self.send_button.pack(pady=5)

    def update_status(self, msg):
        """Update status display in GUI."""
        if self.status_label:
            self.root.after(0, lambda: self.status_label.config(text=msg))

    def display_output(self, msg):
        """Display messages in the output text widget."""
        if self.output_text:
            self.root.after(0, lambda: self._append_to_output(msg))

    def _append_to_output(self, msg):
        """Thread-safe method to append text to output widget."""
        self.output_text.insert(tk.END, f"{msg}\n")
        self.output_text.see(tk.END)

    def send_command(self):
        """Handle manual command from GUI entry."""
        if self.entry:
            cmd = self.entry.get()
            self.entry.delete(0, tk.END)
            self.display_output(f"You entered: {cmd}")
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

    def _run_gui(self):
        """Run the GUI main loop."""
        self.root = tk.Tk()
        self.root.title("Jarvis HUD")
        self.create_widgets()
        
        # Start command processing
        self.process_commands()
        
        # Run the main loop
        self.root.mainloop()

    def start(self):
        """Run the GUI main loop in a separate thread."""
        self.gui_thread = threading.Thread(target=self._run_gui, daemon=True)
        self.gui_thread.start()

    def stop(self):
        """Stop the GUI."""
        self.running = False
        if self.root:
            self.root.quit() 