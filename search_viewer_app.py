import os
import streamlit as st
import configparser
import requests
import datetime
import json
import re

# this must be at the top
st.set_page_config(layout="wide")

# config.toml 파일 경로
CONFIG_FILE = './.streamlit/config.toml'

# # config.toml 파일을 읽어옴
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

with st.sidebar:
    config.read(CONFIG_FILE)
    theme_option = st.radio("Select Light/Dark mode", ["Light", "Dark"])
    if st.button("Double click to Rerun (Light/Dark)"):

        if theme_option == "Light":
            config.set('theme', 'base', '\"light\"')

        if theme_option == "Dark":
            config.set('theme', 'base', '\"dark\"')

        with open(CONFIG_FILE, 'w') as f:
            config.write(f)

        st.cache_resource()

# Create two columns
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("<p style='display: flex; justify-content: center'><img src='https://bpb-us-e1.wpmucdn.com/blogs.cornell.edu/dist/8/7752/files/2021/02/arxiv-logo-1.png' width='150'></p>", unsafe_allow_html=True)
with col2:
    st.title("Paper Search App")

st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    search_type = st.radio("Select the search type", [
        "RO: Robotics", "CV: Computer Vision and Pattern Recognition",
                        "AI: Artificial Intelligence", "LG: Machine Learning"])
with col2:
    AND_or_OR = st.radio("Select OR or AND", ["OR", "AND"])

st.markdown("<hr>", unsafe_allow_html=True)

keywords = st.text_input("🔍 Enter keywords separated by commas")
keywords = keywords.split(",")

if all(len(keyword) >= 2 for keyword in keywords):

    st.write("🍀 10 items per page")

    search_type_key = search_type[:2]
    url = f"http://127.0.0.1:8000/{search_type_key}/keywords/{AND_or_OR}/{','.join(keywords)}"
    response = requests.get(url)
    try:
        json_data = json.loads(response.text)
        total_count = len(json_data)
        page_size = 10
        num_pages = (total_count - 1) // page_size + 1

        current_page = st.sidebar.number_input(
            "Enter a page number", min_value=1, max_value=num_pages, value=1
        )
        start_index = (current_page - 1) * page_size
        end_index = min(start_index + page_size, total_count)

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

        for i, (key, val) in enumerate(list(json_data.items())[start_index:end_index]):
            col1, col2, col3, col4 = st.columns([0.5, 2, 5, 0.5])
            created_at = str(val[0])
            summary = val[1]
            link = val[2]
            with col1:
                st.markdown(
                    f"<p style='text-align: center'>{created_at[:4]}<br>{created_at[5:10]}</p>", unsafe_allow_html=True)
            with col2:
                highlighted_key = highlight_keyword(key, keywords)
                st.markdown(
                    f"<div style='font-weight: bold;'>{highlighted_key}</div>", unsafe_allow_html=True)
            with col3:
                highlighted_summary = highlight_keyword(summary, keywords)
                st.markdown(highlighted_summary, unsafe_allow_html=True)
            with col4:
                st.write(link)

        st.sidebar.markdown(
            f"Page {current_page} of {num_pages}")

    except ValueError as e:
        st.write("Error loading JSON:", e)
else:
    st.write("Please enter at least two alphabets for each keyword.")


st.markdown("<hr>", unsafe_allow_html=True)

st.write("Author: gisbi.kim@gmail.com")

last_modified = os.path.getmtime(__file__)
st.write("Last update: ", datetime.datetime.fromtimestamp(
    last_modified).strftime("%Y-%m-%d"))
