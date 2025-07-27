import tkinter as tk
from tkinter import ttk

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Counter App")
        self.root.geometry("300x200")

        self.count = 0

        # Label to display counter
        self.label = ttk.Label(root, text=f"Count: {self.count}")
        self.label.pack(pady=20)

        # Buttons
        self.inc_button = ttk.Button(root, text="Increment", command=self.increment)
        self.inc_button.pack(pady=5)
        self.dec_button = ttk.Button(root, text="Decrement", command=self.decrement)
        self.dec_button.pack(pady=5)
        self.reset_button = ttk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

    def increment(self):
        self.count += 1
        self.label.config(text=f"Count: {self.count}")

    def decrement(self):
        self.count -= 1
        self.label.config(text=f"Count: {self.count}")

    def reset(self):
        self.count = 0
        self.label.config(text=f"Count: {self.count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()
