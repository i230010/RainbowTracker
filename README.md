# RainbowTracker

This app shows the positions of Rainbow and Moonbow in Python

The project uses **Skyfield** for astronomical calculations

## Requirements

- Python 3.x
- JPL Development Ephemerides (DEXXX) files located in local directory (already included)
- Windows 11 ONLY

## How to use the app

Click the left mouse and Drag to view the positions. Click the "+" or "-" to add or sub seconds, minutes, hours. Click the "Now" to undo all changes of time to current time. The "Stop" pauses and unpauses the time.

## How to Run (.exe file)

Go to the releases section, Download the latest version of the RainbowTrackerExecutable and click the `main.exe`

## How to Run (Raw python file)

This project supports execution using **uv**, a fast Python package manager and runner.

To run the main Eclipse computation script (on the folder):

```bash
uv run main.py
```

After doing some changes and you want to convert back to a normal .exe file, use this command `pyinstaller main.pyw --onefile --windowed --collect-all panda3d --collect-all ursina` and put the `DejaVuSans.ttf`, `icon.ico` and your `dexxx.bsp` file in the dist folder