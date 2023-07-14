import sqlite3
from tabulate import tabulate

# SQLite database
conn = sqlite3.connect('verification.db')
cursor = conn.cursor()

# Retrieve data from the database
cursor.execute("SELECT email, password, time FROM verification")
data = cursor.fetchall()

# Print the database contents as a table
headers = ["Email", "Password", "Time"]
table = tabulate(data, headers=headers, tablefmt="grid")
print(table)

conn.close()
