import tkinter as tk
from tkinter import ttk
import random  # For simulation; replace with actual sensor library
import time

class TempApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Monitor")
        self.root.geometry("300x100")

        # Label to display temperature
        self.temp_label = ttk.Label(root, text="Temperature: N/A °C")
        self.temp_label.pack(pady=20)

        # Start updating temperature
        self.update_temperature()

    def update_temperature(self):
        # Simulate temperature (replace with real sensor reading, e.g., TMP102)
        temperature = random.uniform(20.0, 30.0)  # Simulated value
        self.temp_label.config(text=f"Temperature: {temperature:.1f} °C")
        # Schedule next update
        self.root.after(2000, self.update_temperature)

if __name__ == "__main__":
    root = tk.Tk()
    app = TempApp(root)
    root.mainloop()
