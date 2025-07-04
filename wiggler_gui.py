import ctypes
import sys
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class MouseWigglerGUI(tk.Tk):    def __init__(self):
        super().__init__()

        self.running = True
        self.paused = False
        
        # Windows API constants
        self.MOUSEEVENTF_MOVE = 0x0001
        self.user32 = ctypes.windll.user32
        
        # Configure window
        self.title("Mouse Wiggler")
        self.geometry("300x150")
        self.configure(bg='white')
        
        # Make window stay on top
        self.attributes('-topmost', True)
        
        # Create controls
        self.create_widgets()
        
        # Start mouse movement thread
        self.movement_thread = threading.Thread(target=self.wiggle_mouse, daemon=True)
        self.movement_thread.start()
        
        # Bind close button
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window on screen
        self.center_window()
    
    def create_tray_icon(self):
        # Create a simple icon (a filled circle)
        icon_size = 64
        icon_image = Image.new('RGB', (icon_size, icon_size), color='white')
        drawing = ImageDraw.Draw(icon_image)
        drawing.ellipse([8, 8, icon_size-8, icon_size-8], fill='green')
        
        # Create system tray menu
        menu = (
            pystray.MenuItem("Show/Hide", self.toggle_window),
            pystray.MenuItem("Pause/Resume", self.toggle_pause),
            pystray.MenuItem("Exit", self.stop),
        )
        
        self.icon = pystray.Icon("wiggler", icon_image, "Mouse Wiggler", menu)
    
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
        state = "paused" if self.paused else "resumed"
        self.icon.notify(f"Mouse Wiggler {state}")
    
    def toggle_window(self):
        self.hidden = not self.hidden
    
    def stop(self):
        self.running = False
        self.icon.stop()
        sys.exit(0)
    
    def run(self):
        self.icon.run()

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
        app.run()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            f.write(f"Error occurred: {str(e)}\n")
            f.write(traceback.format_exc())
