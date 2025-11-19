import psycopg2
import pandas as pd
import os
import time

# Wait for DB to be ready
time.sleep(20)

# Load CSV
df = pd.read_csv("seed/books_cleaned.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS book (
    isbn TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    "language" TEXT,
    data_source TEXT,
    description TEXT
);
"""

cur.execute(create_table_sql)
conn.commit()
print("Table created successfully.")

for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO book (isbn, title, author, genre, "language", data_source, description)
            VALUES (%s, %s, %s, %s, %s, %s, NULL)
            ON CONFLICT (isbn) DO NOTHING;
        """, (
            str(row["ISBN"]),
            row["title"],
            row["author"],
            row["genre"],
            row["language"],
            row["data_source"]
        ))
    except Exception as e:
        print("ERROR ROW:", row)
        print("ERROR MSG:", e)
        conn.rollback()
        break

conn.commit()
cur.close()
conn.close()
print("All books inserted successfully.")
