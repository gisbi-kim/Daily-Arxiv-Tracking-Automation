# Daily Arxiv Automation
## Features 
### 1. Automatically parse a daily arxiv rss
  - a. parse information and save into the database (sqlite3)
  - b. (optional) download the all pdfs
    - with auto-naming as {YY} {Title}
    - example
      - <img width="488" alt="image" src="https://user-images.githubusercontent.com/14989535/221883912-90e6c89b-1b51-498a-b51b-969736575140.png">
  - TODO: 
    - This DB growing (appending) will be automatically done via Github Action.

### 2. Search web app
- Just do `run_app.sh` 
  - The dependencies: fastapi, uvicorn, and streamlit
