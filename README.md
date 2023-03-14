[![Run arxiv_saver_to_db.py and commit changes](https://github.com/gisbi-kim/daily_arxiv_automation/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/gisbi-kim/daily_arxiv_automation/actions/workflows/main.yml)

# Daily Arxiv Automation
## Features 
### 1. Automatically parse a daily arxiv rss
  - a. parse information and save into the database (sqlite3)
    - This DB is automatically growing (appending) via Github Action.
  - b. (optional) download the all pdfs
    - with auto-naming as {YY} {Title}
    - example
      - <img width="488" alt="image" src="https://user-images.githubusercontent.com/14989535/221883912-90e6c89b-1b51-498a-b51b-969736575140.png">

### 2. Search web app
- Just do `run_app.sh` 
  - The dependencies: fastapi, uvicorn, and streamlit
