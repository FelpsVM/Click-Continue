# Continuous Clicker Script

This Python script uses the `pynput` and `pyautogui` libraries to simulate continuous left mouse clicks when the "Delete" key is pressed. It runs in the background and can be toggled on/off by pressing the "Delete" key.

## Features

- **Automatic Clicker**: Hold the "Delete" key to simulate continuous left mouse clicks.
- **Toggle On/Off**: Press the "Delete" key to activate or deactivate the automatic clicking.
- **Multithreaded**: The script uses threading to ensure smooth clicking without freezing the main application.

## Requirements

Before running the script, make sure you have the required dependencies installed. You can install them via `pip`:

```bash
pip install pynput pyautogui
