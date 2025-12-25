import pyautogui
import time

def send_teams_message(contact_name, message):
    # Step 1: Focus search bar (Ctrl+E in Teams)
    pyautogui.hotkey("command", "e")
    time.sleep(1)

    # Step 2: Type friend's name
    pyautogui.typewrite(contact_name)
    time.sleep(1)

    # Step 3: Press Enter to open chat
    pyautogui.press("enter")
    time.sleep(1)

    # Step 4: Type message and send
    pyautogui.typewrite(message)
    pyautogui.press("enter")

# Example usage
send_teams_message("vamsee mede", "Hi 👋")

