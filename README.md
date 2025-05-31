# Mouse Wiggler

A simple Python script that keeps your computer active by automatically moving the mouse cursor in a small square pattern.

There are three versions available:
1. `wiggler.py` - Regular version using PyAutoGUI
2. `wiggler_standalone.py` - Standalone version using only Python standard library (Windows only)
3. `wiggler_gui.py` - GUI version with system tray icon and pause functionality (Windows only)

## Features

- Moves the mouse cursor in a small square pattern every 30 seconds
- Displays timestamp for each movement
- Includes safety features to easily stop the program

## Requirements

- Python 3.x
- PyAutoGUI library

## Installation

1. Clone or download this repository
2. Install the required package:
```
pip install -r requirements.txt
```

## Usage

### Regular Version
Run the script using Python:
```
python wiggler.py
```

### Standalone Version (Windows Only)
Run the standalone version that doesn't require any additional packages:
```
python wiggler_standalone.py
```

### GUI Version (Windows Only)
Double-click the "Start Mouse Wiggler.bat" file or run:
```
pythonw wiggler_gui.py
```

The GUI version runs in the system tray with the following features:
- Right-click the tray icon for menu options
- Pause/Resume functionality
- Hidden console window
- Failsafe (move mouse to top-left corner to exit)

### How to Stop

There are two ways to stop the program:
1. Press `Ctrl+C` in the terminal
2. Quickly move your mouse cursor to the top-left corner of the screen (failsafe feature)

## Safety Features

- Built-in failsafe: Moving your mouse to the top-left corner of the screen will stop the program
- The mouse movements are small and controlled
- Each movement is visible and takes 0.5 seconds to complete

## Note

This script is intended for legitimate use cases where keeping your computer active is necessary. Please use responsibly and in accordance with your organization's policies.
