import tkinter as tk
from tkinter import ttk

class CalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x250")

        # Entry fields for numbers
        self.label1 = ttk.Label(root, text="Enter first number:")
        self.label1.pack(pady=5)
        self.entry1 = ttk.Entry(root)
        self.entry1.pack(pady=5)

        self.label2 = ttk.Label(root, text="Enter second number:")
        self.label2.pack(pady=5)
        self.entry2 = ttk.Entry(root)
        self.entry2.pack(pady=5)

        # Result label
        self.result_label = ttk.Label(root, text="Result: ")
        self.result_label.pack(pady=10)

        # Buttons for operations
        self.add_button = ttk.Button(root, text="Add", command=self.add)
        self.add_button.pack(pady=5)
        self.sub_button = ttk.Button(root, text="Subtract", command=self.subtract)
        self.sub_button.pack(pady=5)

    def add(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 + num2
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            self.result_label.config(text="Result: Invalid input")

    def subtract(self):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            result = num1 - num2
            self.result_label.config(text=f"Result: {result}")
        except ValueError:
            self.result_label.config(text="Result: Invalid input")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalcApp(root)
    root.mainloop()
