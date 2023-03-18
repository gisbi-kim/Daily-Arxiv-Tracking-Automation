import os
import streamlit as st
import configparser
import requests
import datetime
import json
import re


def spawn_darkmode_sidebar():
    # config.toml 파일 경로
    CONFIG_FILE = './.streamlit/config.toml'

    # # config.toml 파일을 읽어옴
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    with st.sidebar:
        config.read(CONFIG_FILE)
        theme_option = st.radio("Select Light/Dark mode", ["Light", "Dark"])
        if st.button("Double-click to change (Light/Dark)"):

            if theme_option == "Light":
                config.set('theme', 'base', '\"light\"')

            if theme_option == "Dark":
                config.set('theme', 'base', '\"dark\"')

            with open(CONFIG_FILE, 'w') as f:
                config.write(f)

            st.cache_resource()


def spawn_title():
    # Create two columns
    col1, col2 = st.columns([1, 4])
    with col1:
        img_src = "<img src='https://bpb-us-e1.wpmucdn.com/blogs.cornell.edu/dist/8/7752/files/2021/02/arxiv-logo-1.png' width='170'>"
        st.markdown(f"<p style='display: flex; justify-content: center'>{img_src}</p>",
                    unsafe_allow_html=True)
    with col2:
        st.title("Paper Search App")


def gray_line():
    st.markdown("<hr>", unsafe_allow_html=True)


def spawn_selection_options():
    col1, col2 = st.columns([1, 2])
    with col1:
        search_type = st.radio("Select the search type", [
            "RO: Robotics",
            "CV: Computer Vision and Pattern Recognition",
            "AI: Artificial Intelligence",
            "LG: Machine Learning"])
    with col2:
        AND_or_OR = st.radio("Select OR or AND", ["OR", "AND"])

    return search_type, AND_or_OR


def spawn_search_zone():
    keywords = st.text_input("🔍 Enter keywords separated by commas")
    keywords = keywords.split(",")
    return keywords


def get_data_from_server(table_to_search, AND_or_OR, keywords):
    url = f"http://127.0.0.1:8000/{table_to_search}/keywords/{AND_or_OR}/{','.join(keywords)}"
    response = requests.get(url)
    return json.loads(response.text)


def all_keywords_has_more_including_than_k_len(keywords, k):
    return all(len(keyword) >= k for keyword in keywords)


def spawn_column_names():
    col1, col2, col3, col4 = st.columns([0.5, 2, 5, 0.5])
    with col1:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>Date</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>Title</p>", unsafe_allow_html=True)
    with col3:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>Abstract</p>", unsafe_allow_html=True)
    with col4:
        st.markdown(
            f"<p style='text-align: center; font-weight: bold;'>Link</p>", unsafe_allow_html=True)


def highlight_keyword(text, keywords):
    pattern = re.compile('|'.join(keywords), flags=re.IGNORECASE)
    highlighted_text = pattern.sub(
        lambda x: f"<mark style='background-color: #ffffb3;'>{x.group()}</mark>", text)
    return highlighted_text


def spawn_item_row(item, keywords):
    key, val = item
    created_at = str(val[0])
    created_at_yyyy = created_at[:4]
    created_at_mmdd = created_at[5:10]
    summary = val[1]
    link_pdf = val[2]

    col1, col2, col3, col4 = st.columns([0.5, 2, 5, 0.5])
    with col1:
        st.markdown(
            f"<p style='text-align: center'>{created_at_yyyy}<br>{created_at_mmdd}</p>", unsafe_allow_html=True)
    with col2:
        highlighted_key = highlight_keyword(key, keywords)
        st.markdown(
            f"<div style='font-weight: bold;'>{highlighted_key}</div>", unsafe_allow_html=True)
    with col3:
        highlighted_summary = highlight_keyword(summary, keywords)
        st.markdown(highlighted_summary, unsafe_allow_html=True)
    with col4:
        st.write(
            f"<div style='text-align: center;'><a href='{link_pdf}'>pdf</a></div>", unsafe_allow_html=True)
        link_abs = link_pdf.replace("pdf", "abs")[:-4]
        st.write(
            f"<div style='text-align: center;'><a href='{link_abs}'>abs</a></div>", unsafe_allow_html=True)


def spawn_sidebar_md(msg):
    st.sidebar.markdown(msg)


def spawn_info():
    st.write("Author: gisbi.kim@gmail.com")

    last_modified = os.path.getmtime(__file__)
    st.write("Last update: ", datetime.datetime.fromtimestamp(
        last_modified).strftime("%Y-%m-%d"))
