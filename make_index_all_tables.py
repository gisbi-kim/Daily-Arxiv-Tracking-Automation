import sqlite3

db_path = "arxiv_papers.sqlite3"

print("start indexing ...")
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # 모든 테이블 이름을 조회
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()

    for table_name in table_names:
        # 각 테이블에 대해 색인 생성
        try:
            cursor.execute(f"PRAGMA table_info({table_name[0]})")
            column_names = cursor.fetchall()
            for column_name in column_names:
                cursor.execute(
                    f"CREATE INDEX idx_{table_name[0]}_{column_name[1]} ON {table_name[0]} ({column_name[1]});")
        except:
            print(f" This {table_name} had already been indexed.")

print("end indexing.")
