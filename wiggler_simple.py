import ctypes
import sys
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class MouseWigglerGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.running = True
        self.paused = False
        
        # Windows API constants
        self.MOUSEEVENTF_MOVE = 0x0001
        self.user32 = ctypes.windll.user32
        
        # Configure window
        self.title("Mouse Wiggler")
        self.geometry("300x100")
        self.configure(bg='lightgray')
        
        # Create GUI elements
        self.create_widgets()
        
        # Start mouse movement thread
        self.movement_thread = threading.Thread(target=self.wiggle_mouse, daemon=True)
        self.movement_thread.start()
        
        # Bind close button
        self.protocol("WM_DELETE_WINDOW", self.stop)
        
        # Center window
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Status label
        self.status_var = tk.StringVar(value="Running")
        status_label = ttk.Label(self, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Control buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)
        
        # Pause/Resume button
        self.toggle_button = ttk.Button(button_frame, text="Pause", command=self.toggle_pause)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        exit_button = ttk.Button(button_frame, text="Exit", command=self.stop)
        exit_button.pack(side=tk.LEFT, padx=5)
    
    def get_cursor_pos(self):
        point = ctypes.wintypes.POINT()
        self.user32.GetCursorPos(ctypes.byref(point))
        return (point.x, point.y)
    
    def move_mouse_relative(self, dx, dy):
        self.user32.mouse_event(self.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
    
    def wiggle_mouse(self):
        while self.running:
            if not self.paused:
                # Get current position
                start_x, start_y = self.get_cursor_pos()
                
                # Check failsafe (top-left corner)
                if start_x < 5 and start_y < 5:
                    self.stop()
                    break
                
                # Move in square pattern
                for _ in range(2):
                    if not self.paused and self.running:
                        self.move_mouse_relative(10, 0)
                        time.sleep(0.5)
                        self.move_mouse_relative(0, 10)
                        time.sleep(0.5)
                        self.move_mouse_relative(-10, 0)
                        time.sleep(0.5)
                        self.move_mouse_relative(0, -10)
                        time.sleep(0.5)
            
            # Wait before next movement
            time.sleep(30)
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.status_var.set("Paused")
            self.toggle_button.configure(text="Resume")
        else:
            self.status_var.set("Running")
            self.toggle_button.configure(text="Pause")
    
    def stop(self):
        self.running = False
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    try:
        # Hide console window
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0)
        
        # Start application
        app = MouseWigglerGUI()
        app.mainloop()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(f"Error occurred: {str(e)}\n")
            f.write(traceback.format_exc())
