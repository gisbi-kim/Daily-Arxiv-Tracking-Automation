import sqlite3

db_path = "arxiv_papers.sqlite3"
table_name = "RO"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    print(f"table_names {table_names}")
    assert 0 < len(
        table_names), 'please using python3 db_utils/this_file.py at the parent path.'

    cursor.execute(f"PRAGMA index_list({table_name})")
    index_list = cursor.fetchall()

if len(index_list) > 0:
    print("Index exists")
else:
    print("No indexed")
