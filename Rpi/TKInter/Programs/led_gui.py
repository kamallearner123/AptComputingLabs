import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO

class LEDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Controller")
        self.root.geometry("300x150")

        # Setup GPIO
        self.GPIO20 = 20
        self.GPIO21 = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO20, GPIO.OUT)
        GPIO.setup(self.GPIO21, GPIO.OUT)
        self.led20_state = False
        self.led21_state = False

        # GUI Elements
        ttk.Label(root, text="Control LEDs on GPIO 20 and 21").pack(pady=10)
        self.btn20 = ttk.Button(root, text="Toggle LED 20 (OFF)", command=self.toggle_led20)
        self.btn20.pack(pady=5)
        self.btn21 = ttk.Button(root, text="Toggle LED 21 (OFF)", command=self.toggle_led21)
        self.btn21.pack(pady=5)
        ttk.Button(root, text="Exit", command=self.exit).pack(pady=5)

    def toggle_led20(self):
        self.led20_state = not self.led20_state
        GPIO.output(self.GPIO20, GPIO.HIGH if self.led20_state else GPIO.LOW)
        self.btn20.config(text=f"Toggle LED 20 ({'ON' if self.led20_state else 'OFF'})")

    def toggle_led21(self):
        self.led21_state = not self.led21_state
        GPIO.output(self.GPIO21, GPIO.HIGH if self.led21_state else GPIO.LOW)
        self.btn21.config(text=f"Toggle LED 21 ({'ON' if self.led21_state else 'OFF'})")

    def exit(self):
        GPIO.cleanup()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDApp(root)
    root.mainloop()
