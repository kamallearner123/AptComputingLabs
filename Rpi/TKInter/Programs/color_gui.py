import tkinter as tk
from tkinter import ttk

class ColorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Changer")
        self.root.geometry("300x200")

        # Variable to store selected color
        self.color_var = tk.StringVar(value="white")

        # Label
        self.label = ttk.Label(root, text="Select a background color:")
        self.label.pack(pady=10)

        # Radio buttons for color selection
        colors = ["white", "red", "blue", "green"]
        for color in colors:
            ttk.Radiobutton(
                root, 
                text=color.capitalize(), 
                value=color, 
                variable=self.color_var, 
                command=self.change_color
            ).pack(anchor="w", padx=20)

    def change_color(self):
        self.root.configure(bg=self.color_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorApp(root)
    root.mainloop()
