import tkinter as tk
from tkinter import ttk, filedialog

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("400x400")

        # Text widget
        self.text_area = tk.Text(root, height=15, width=40)
        self.text_area.pack(pady=10)

        # Buttons
        self.save_button = ttk.Button(root, text="Save File", command=self.save_file)
        self.save_button.pack(pady=5)
        self.load_button = ttk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=5)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get("1.0", tk.END))
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "File saved!")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", content)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
