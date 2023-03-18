import streamlit as st
import requests
import json

st.set_page_config(layout="wide")

st.title("arxiv paper search app")

search_type = st.radio("Select the search type", ["ro", "cv", "ai", "lg"])
AND_or_OR = st.radio("Select OR or AND", ["OR", "AND"])

keywords = st.text_input("Enter keywords separated by commas")
keywords = keywords.split(",")

if all(len(keyword) >= 2 for keyword in keywords):
    url = f"http://127.0.0.1:8000/{search_type}/keywords/{AND_or_OR}/{','.join(keywords)}"
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

        col1, col2, col3 = st.columns([1, 2, 5])
        with col1:
            st.markdown(
                f"<p style='text-align: center; font-weight: bold;'>Date</p>", unsafe_allow_html=True)
        with col2:
            st.markdown(
                f"<p style='text-align: center; font-weight: bold;'>Title</p>", unsafe_allow_html=True)
        with col3:
            st.markdown(
                f"<p style='text-align: center; font-weight: bold;'>Abstract</p>", unsafe_allow_html=True)

        for i, (key, val) in enumerate(list(json_data.items())[start_index:end_index]):
            col1, col2, col3 = st.columns([1, 2, 5])
            created_at = str(val[0])
            summary = val[1]
            with col1:
                st.markdown(
                    f"<p style='text-align: center'>{created_at[:10]}</p>", unsafe_allow_html=True)
            with col2:
                st.write(f"**{key}**")
            with col3:
                # st.markdown(
                #     f"<p style='text-align: left'>{summary}</p>", unsafe_allow_html=True)
                st.write(summary)

        st.sidebar.markdown(
            f"Page {current_page} of {num_pages}")

    except ValueError as e:
        st.write("Error loading JSON:", e)
else:
    st.write("Please enter at least two alphabets for each keyword.")
