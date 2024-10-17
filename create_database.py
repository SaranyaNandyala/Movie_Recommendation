import sqlite3
import pandas as pd

# Create a connection to the SQLite database
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Create the movies table
cursor.execute('''
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT NOT NULL
)
''')

# Sample data
movies_data = [
    (1, "The Shawshank Redemption", "Drama"),
    (2, "The Godfather", "Crime,Drama"),
    (3, "The Dark Knight", "Action,Crime,Drama"),
    (4, "Pulp Fiction", "Crime,Drama"),
    (5, "Forrest Gump", "Drama,Romance"),
    (6, "Inception", "Action,Adventure,Sci-Fi"),
    (7, "The Matrix", "Action,Sci-Fi"),
    (8, "Goodfellas", "Biography,Crime,Drama"),
    (9, "The Silence of the Lambs", "Crime,Drama,Thriller"),
    (10, "Schindler's List", "Biography,Drama,History")
]

# Insert the sample data
cursor.executemany("INSERT INTO movies (id, title, genres) VALUES (?, ?, ?)", movies_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created and populated with sample data.")