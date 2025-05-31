import pyautogui
import time
import sys
from datetime import datetime

# Ensure safe exit
pyautogui.FAILSAFE = True

def wiggle_mouse():
    print("Mouse wiggler started! Move mouse to top-left corner to exit.")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Get current time
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Move mouse in a small square pattern
            for _ in range(2):
                pyautogui.moveRel(10, 0, duration=0.5)
                pyautogui.moveRel(0, 10, duration=0.5)
                pyautogui.moveRel(-10, 0, duration=0.5)
                pyautogui.moveRel(0, -10, duration=0.5)
            
            print(f"[{current_time}] Mouse moved")
            
            # Wait for 30 seconds before next movement
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\nMouse wiggler stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    wiggle_mouse()
