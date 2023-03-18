import sqlite3

db_path = "arxiv_papers.sqlite3"
table_name = "AI"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA index_list({table_name})")
    index_list = cursor.fetchall()

if len(index_list) > 0:
    print("Index exists")
else:
    print("No indexed")
