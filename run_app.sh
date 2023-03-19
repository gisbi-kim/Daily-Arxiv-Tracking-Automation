kill_port() {
    lsof -i :8000 | awk 'NR!=1 {print $2}' | xargs kill
    sleep 1
}

kill_port
python3 app/search_server.py &
streamlit run app/search_viewer_app.py
