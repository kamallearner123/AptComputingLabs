import sqlite3

# Set up the SQLite database
connection = sqlite3.connect("menu.db")
cursor = connection.cursor()

# Create a menu_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Insert sample menu items
cursor.execute("INSERT INTO menu_items (name, price) VALUES ('Pizza', 8.99)")
cursor.execute("INSERT INTO menu_items (name, price) VALUES ('Burger', 5.49)")
cursor.execute("INSERT INTO menu_items (name, price) VALUES ('Pasta', 7.99)")
cursor.execute("INSERT INTO menu_items (name, price) VALUES ('Salad', 4.99)")
connection.commit()

cursor.close()
connection.close()
