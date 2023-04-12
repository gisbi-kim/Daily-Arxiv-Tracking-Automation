import os
# os.environ['DISPLAY'] = ':0.0'

import streamlit as st
import configparser
import requests
import datetime
import json
import re
import socket


def is_address_available(address):
    """
    Check if the given address is available.
    :param address: A tuple of (ip, port) representing the address to check.
    :return: True if the address is available, False otherwise.
    """
    try:
        # Create a new socket and try to connect to the address
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set a timeout for the connection attempt
            sock.connect(address)
        return False  # The connection succeeded, so the address is not available
    except ConnectionRefusedError:
        return True  # The connection failed, so the address is available


def spawn_empty_sidebar():
    with st.sidebar:
        st.markdown("<p style='color: #5e5e5e'>Tip: For <strong>dark</strong> mode, go to <code>Settings</code> at the top-right menu.</p>",
                    unsafe_allow_html=True)

        st.markdown("<hr style='margin: 5px 0px; 'border: 1px solid #d9d9d9;'>",
                    unsafe_allow_html=True)


def spawn_darkmode_sidebar():
    CONFIG_FILE = './.streamlit/config.toml'
    config = configparser.ConfigParser()
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
        st.title(f"Paper Search App")


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


def get_data_from_server(table_to_search, AND_or_OR, keywords, time_order=True):
    url = f"http://127.0.0.1:8000/{table_to_search}/keywords/{AND_or_OR}/{','.join(keywords)}"
    response = requests.get(url)
    json_data = json.loads(response.text)
    if time_order:
        date_idx = 0
        sorted_json_data = sorted(json_data.items(),
                                  key=lambda item: item[1][date_idx],
                                  reverse=True)
        json_data = dict(sorted_json_data)
    return json_data


def all_keywords_has_more_including_than_k_len(keywords, k):
    return all(len(keyword) >= k for keyword in keywords)


def spawn_column_names():
    def centered_msg(msg):
        return f"<p style='text-align: center; font-weight: bold;'>{msg}</p>"

    col1, col2, col3, col4 = st.columns([0.5, 2.0, 5.0, 0.5])
    with col1:
        st.markdown(centered_msg("Data"), unsafe_allow_html=True)
    with col2:
        st.markdown(centered_msg("Title"), unsafe_allow_html=True)
    with col3:
        st.markdown(centered_msg("Abstract"), unsafe_allow_html=True)
    with col4:
        st.markdown(centered_msg("Link"), unsafe_allow_html=True)


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

    col1, col2, col3, col4 = st.columns([0.5, 2.0, 5.0, 0.5])
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


def go_top():

    st.markdown(
        """
        <style>
            .back-to-top {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 100;
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #3B3B3B;
                border: none;
                border-radius: 50%;
                padding: 20px;
                cursor: pointer;
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
                opacity: 0.7;
                transition: opacity 0.2s ease-in-out;
            }
            .back-to-top:hover {
                opacity: 1;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        '<a href="#paper-search-app" class="back-to-top">^</a>', unsafe_allow_html=True)


def spawn_info():
    st.write("Author: [gisbi.kim@gmail.com](https://bit.ly/giseopkim)")
    last_modified = os.path.getmtime(__file__)
    st.write("[Last update](https://github.com/gisbi-kim/Daily-Arxiv-Tracking-Automation): ", datetime.datetime.fromtimestamp(
        last_modified).strftime("%Y-%m-%d"))
