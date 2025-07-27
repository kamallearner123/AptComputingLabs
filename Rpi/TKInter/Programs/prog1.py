import tkinter as tk
import requests
from tkinter import ttk



#Create a window
window = tk.Tk()
#Add all the widgets
window.title("Welcome to hackers hub")
l1 = tk.Label(window, text="Initial Test", font = ("Arial bold", 34))

l1.grid(column=0, row=0)
window.geometry('200x300')

option = ttk.Combobox(window, values=["https://www.bbc.com", "https://www.cnn.com"])
option.grid(column=0, row=1)


def function1():
    url = option.get()
    content = requests.get(url) # https://www.bbc.com
    text = content.text
    l2 = tk.Label(window, text=text[:1000], font=("Arial", 20), wraplength=200)
    l2.grid(column=1, row=1)

# # Adding text input field
# e1 = tk.Entry(window, width=20)
# e1.grid(column=0, row=1)
# # Adding a label for the input field
# l2 = tk.Label(window, text="Enter website url", font=("Arial", 12))
# l2.grid(column=0, row=2)



# Button
b1 = tk.Button(window, text = "Get Some News", command = function1)
b1.grid(column=1, row=0)


#Start window in loop
window.mainloop()
