import uvicorn
import subprocess
import os
import streamlit as st
import configparser
import requests
import datetime
import json
import re
from search_viewer_app_lib import *

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
            link = row[3]
            created_at = row[4]
            result[title] = [created_at, summary, link]

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
        link = row[3]
        created_at = row[4]
        created_at = row[-1]
        if all(kw.lower() in (title + summary).lower() for kw in keywords):
            result[title] = [created_at, summary, link]

    conn.close()

    return result


if is_address_available(('127.0.0.1', 8000)):
    uvicorn.run(app, host="127.0.0.1", port=8000)
else:
    print("The server is already running. no need to restart it.")


st.set_page_config(
    layout="wide",
    page_title="arxiv searcher",
    page_icon=":house:",
    initial_sidebar_state="expanded"
)

spawn_darkmode_sidebar()
spawn_title()
gray_line()

search_type, AND_or_OR = spawn_selection_options()
gray_line()

col1, col2 = st.columns([2, 1])
with col1:
    keywords = spawn_search_zone()

if not all_keywords_has_more_including_than_k_len(keywords, 2):
    st.write("Please enter at least two alphabets for each keyword.")
else:
    DEFAULT_NUM_PAPERS_PER_PAGE = 10
    with col2:
        page_size = st.selectbox("Select the number of papers per page", [
            5, 10, 15, 20, 30, 50], index=1)
    NUM_PAPERS_PER_PAGE = page_size or DEFAULT_NUM_PAPERS_PER_PAGE
    st.write(
        f"🍀 {NUM_PAPERS_PER_PAGE} items per page (recent one is displayed first)")

    table_to_search = search_type[:2]
    json_data = get_data_from_server(table_to_search, AND_or_OR, keywords)

    total_count = len(json_data)
    num_pages = (total_count - 1) // NUM_PAPERS_PER_PAGE + 1

    try:
        current_page = st.sidebar.number_input(
            "Enter a page number", min_value=1, max_value=num_pages, value=1
        )
        start_index = (current_page - 1) * NUM_PAPERS_PER_PAGE
        end_index = min(start_index + NUM_PAPERS_PER_PAGE, total_count)

        spawn_column_names()
        for i, item in enumerate(list(json_data.items())[start_index:end_index]):
            spawn_item_row(item, keywords)

        spawn_sidebar_md(f"Page {current_page} of {num_pages}")

    except ValueError as e:
        st.write("Error loading JSON:", e)

gray_line()
spawn_info()
