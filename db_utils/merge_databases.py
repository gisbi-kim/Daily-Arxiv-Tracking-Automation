import datetime
import sqlite3
import os

# 현재 디렉토리에서 "arxiv_papers_YYYY-MM-DD.sqlite3" 파일들을 모두 읽어온다
db_files = [f for f in os.listdir('.') if f.startswith(
    'arxiv_papers') and f.endswith('.sqlite3')]
print(f"db_files: {db_files}")

# "combined_db.sqlite3" 파일이 존재하면 삭제한다
if os.path.isfile('combined_db.sqlite3'):
    os.remove('combined_db.sqlite3')

# "combined_db.sqlite3" 파일을 생성하고, 모든 테이블에 대해 새로운 논문 정보를 추가한다
conn = sqlite3.connect('combined_db.sqlite3')
for db_file in db_files:
    db_conn = sqlite3.connect(db_file)
    db_cursor = db_conn.cursor()
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in db_cursor.fetchall()]
    assert 0 < len(
        tables), 'please using python3 db_utils/merge_databases.py at the parent path.'
    for table in tables:
        db_cursor.execute(
            f"SELECT title, year, summary, link, created_at FROM {table}")
        papers = db_cursor.fetchall()
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} (title TEXT, year INTEGER, summary TEXT, link TEXT, created_at TIMESTAMP)")
        for paper in papers:
            cursor.execute(f"SELECT * FROM {table} WHERE title=?", (paper[0],))
            if not cursor.fetchone():
                datum_info = '(title, year, summary, link, created_at)'

                t = paper[4]
                created_time = datetime.datetime(
                    int(t[:4]), int(t[5:7]), int(t[8:10]),
                    int(t[11:13]), int(t[14:16]), int(t[17:19]), 0)

                datum = (paper[0], paper[1], paper[2], paper[3], created_time)
                cursor.execute(
                    f"INSERT INTO {table} {datum_info} VALUES (?, ?, ?, ?, ?)", datum)
        conn.commit()
    db_conn.close()
conn.close()

print("The merged (non-indexed) file is generated.")
