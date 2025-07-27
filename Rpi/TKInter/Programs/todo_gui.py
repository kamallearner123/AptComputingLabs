import tkinter as tk
from tkinter import ttk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("300x400")

        # Entry for new tasks
        self.task_entry = ttk.Entry(root)
        self.task_entry.pack(pady=10)

        # Add task button
        self.add_button = ttk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(root, height=15, width=30)
        self.task_listbox.pack(pady=10)

        # Clear tasks button
        self.clear_button = ttk.Button(root, text="Clear All", command=self.clear_tasks)
        self.clear_button.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            self.task_listbox.insert(tk.END, "Error: Empty task")

    def clear_tasks(self):
        self.task_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
