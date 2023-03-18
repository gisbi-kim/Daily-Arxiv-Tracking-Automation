import sqlite3

db_path = "arxiv_papers.sqlite3"

print("start removing indexes ...")
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # 모든 테이블 이름을 조회
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    print(f"table_names {table_names}")
    assert 0 < len(
        table_names), 'please using python3 db_utils/this_file.py at the parent path.'
    for table_name in table_names:
        # 각 인덱스 이름을 조회
        cursor.execute(f"PRAGMA index_list({table_name[0]})")
        index_names = cursor.fetchall()
        for index_name in index_names:
            if index_name[1] is not None:  # 인덱스 이름이 None이 아닌 경우에만 DROP INDEX문 실행
                cursor.execute(f"DROP INDEX IF EXISTS {index_name[1]};")

print("done")
