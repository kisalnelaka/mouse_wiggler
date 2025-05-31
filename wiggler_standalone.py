import ctypes
import sys
import time
from datetime import datetime

# Windows API constants and functions
MOUSEEVENTF_MOVE = 0x0001

# Load user32.dll for mouse control
user32 = ctypes.windll.user32

def get_cursor_pos():
    point = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return (point.x, point.y)

def set_cursor_pos(x, y):
    user32.SetCursorPos(x, y)

def move_mouse_relative(dx, dy):
    user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)

def wiggle_mouse_standalone():
    print("Standalone Mouse wiggler started!")
    print("Press Ctrl+C to stop")
    print("To force stop, quickly move mouse to top-left corner (0,0)")
    
    try:
        while True:
            # Get current time
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Get current mouse position
            start_x, start_y = get_cursor_pos()
            
            # Check if mouse is in the top-left corner (failsafe)
            if start_x < 5 and start_y < 5:
                print("\nFailsafe activated - mouse in top-left corner")
                sys.exit(0)
            
            # Move mouse in a small square pattern
            for _ in range(2):
                move_mouse_relative(10, 0)
                time.sleep(0.5)
                move_mouse_relative(0, 10)
                time.sleep(0.5)
                move_mouse_relative(-10, 0)
                time.sleep(0.5)
                move_mouse_relative(0, -10)
                time.sleep(0.5)
            
            print(f"[{current_time}] Mouse moved")
            
            # Wait for 30 seconds before next movement
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nMouse wiggler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    wiggle_mouse_standalone()