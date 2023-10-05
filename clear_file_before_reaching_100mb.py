import sys 
import shutil
import sqlite3

def vacuum_database(conn):
    conn.execute("VACUUM;")
    conn.commit()

def get_latest_rows(conn):
    # 테이블 목록 가져오기
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = [t[0] for t in tables]

    for table_name in table_names:
        # 테이블의 모든 열(컬럼) 이름을 가져온다.
        columns = conn.execute(f"PRAGMA table_info({table_name});").fetchall()
        column_names = [c[1] for c in columns]  # [c[2] for c in columns] 대신 [c[1] for c in columns] 사용
        # column_names = [c[2] for c in columns]

        # 일반적으로 "date" 또는 "timestamp"와 같은 이름의 열을 기준으로 최신의 행을 찾습니다.
        # 여기서는 예를 들어 첫번째 열을 기준으로 가장 최근의 데이터를 선택합니다.
        # 실제 환경에 맞게 조정할 수 있습니다.
        latest_row = conn.execute(f"SELECT * FROM {table_name} ORDER BY {column_names[0]} DESC LIMIT 1;").fetchone()

        # 테이블의 모든 데이터를 제거한다.
        conn.execute(f"DELETE FROM {table_name};")

        # 최신의 행만 다시 삽입한다.
        placeholders = ",".join("?" * len(latest_row))
        conn.execute(f"INSERT INTO {table_name} VALUES ({placeholders});", latest_row)

    conn.commit()

def main():
    # arxiv_papers.sqlite3 파일을 arxiv_papers_format.sqlite3로 복사
    cleared_name = "arxiv_papers.sqlite3"
    backup_name = sys.argv[1]
    shutil.copy(cleared_name, backup_name)

    # 복사된 DB 연결
    conn = sqlite3.connect(cleared_name)

    # 가장 최신의 행만 남기기
    get_latest_rows(conn)

    # 데이터베이스 크기 최적화
    vacuum_database(conn)

    # 연결 종료
    conn.close()


if __name__ == "__main__":
    main()

