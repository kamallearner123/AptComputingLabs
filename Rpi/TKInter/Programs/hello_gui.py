import tkinter as tk
from tkinter import ttk

class HelloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hello World GUI")
        self.root.geometry("300x150")

        # Label
        self.label = ttk.Label(root, text="Hello, Tkinter!")
        self.label.pack(pady=20)

        # Button to change text
        self.button = ttk.Button(root, text="Click Me", command=self.change_text)
        self.button.pack(pady=10)

    def change_text(self):
        self.label.config(text="Welcome to Tkinter!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HelloApp(root)
    root.mainloop()
