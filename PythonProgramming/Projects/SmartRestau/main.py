import sqlite3
import tkinter as tk    
from tkinter import *
from tkinter import messagebox


if __name__ == "__main__":
    # Read the menu from "menu.db" and print it to tkinter GUI

    # Create a window
    window = Tk()
    window.title("Smart Restaurant")

    # Create a label
    label = Label(window, text="Menu")
    label.pack()

    # Create a listbox
    listbox = Listbox(window)
    listbox.pack()

    # Connect to the database
    connection = sqlite3.connect("menu.db")
    cursor = connection.cursor()

    # Fetch the menu items
    cursor.execute("SELECT name, price FROM menu_items")
    menu_items = cursor.fetchall()

    # Add the menu items to the listbox
    for name, price in menu_items:
        listbox.insert(END, f"{name}: ${price:.2f}")

    # Close the database connection
    cursor.close()
    connection.close()

    # Run the window
    window.mainloop()




