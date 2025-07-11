import sqlite3

# Connect to database (it will create it if it doesn't exist)
conn = sqlite3.connect("expenses.db")

# Create a table called 'expenses'
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Database and table created successfully.")