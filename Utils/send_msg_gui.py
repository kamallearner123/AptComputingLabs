import pyautogui
import time

def send_teams_message(message, contact_name):
    # Press Ctrl+E to go to search bar in Teams
    pyautogui.hotkey("ctrl", "e")
    time.sleep(1)
    
    # Type contact name
    pyautogui.typewrite(contact_name)
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)

    # Type message
    pyautogui.typewrite(message)
    pyautogui.press("enter")

send_teams_message("Hello! Reminder for your task.", "vamsee mede")

