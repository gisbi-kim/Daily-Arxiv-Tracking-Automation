"""
client side example:
    http://127.0.0.1:8000/ro/keywords/slam
    http://127.0.0.1:8000/cv/keywords/transformer,diffusion
    http://127.0.0.1:8000/ro/keywords/calibration,lidar
"""

from typing import List
from fastapi import FastAPI
import sqlite3
import json

app = FastAPI()
db_path = "arxiv_papers.sqlite3"


@app.get("/{table}/keywords/OR/{keyword}")
async def search_keyword_OR(table: str, keyword: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 키워드 분리
    keywords = keyword.split(',')

    # 결과 저장 딕셔너리 초기화
    result = {}

    # 검색어가 title 혹은 summary에 있는 경우 결과 딕셔너리에 추가
    for kw in keywords:
        c.execute(
            f"SELECT * FROM {table} WHERE title LIKE '%{kw}%' OR summary LIKE '%{kw}%'")
        rows = c.fetchall()
        for row in rows:
            title = row[0]
            summary = row[2]
            result[title] = summary

    conn.close()

    return result


@app.get("/{table}/keywords/AND/{keyword}")
async def search_keyword_AND(table: str, keyword: str):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 키워드 분리
    keywords = keyword.split(',')

    # 결과 저장 딕셔너리 초기화
    result = {}

    # 검색어가 title 혹은 summary에 모두 있는 경우 결과 딕셔너리에 추가
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    for row in rows:
        title = row[0]
        summary = row[2]
        if all(kw.lower() in (title + summary).lower() for kw in keywords):
            result[title] = summary

    conn.close()

    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
