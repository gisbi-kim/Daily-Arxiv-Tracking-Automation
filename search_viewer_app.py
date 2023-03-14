import streamlit as st
import requests
import json


st.title("arxiv paper search app")

search_type = st.radio("Select the search type", ["ro", "cv", "ai"])
AND_or_OR = st.radio("Select AND or OR", ["AND", "OR"])

keywords = st.text_input("Enter keywords separated by commas")
keywords = keywords.split(",")
if all(len(keyword) >= 2 for keyword in keywords):
    url = f"http://127.0.0.1:8000/{search_type}/keywords/{AND_or_OR}/{','.join(keywords)}"
    response = requests.get(url)
    try:
        json_data = json.loads(response.text)
        for key, val in json_data.items():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**{key}**")
            with col2:
                st.write(val)
    except ValueError as e:
        st.write("Error loading JSON:", e)
else:
    st.write("Please enter at least two alphabets for each keyword.")
