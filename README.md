[![Run arxiv_saver_to_db.py and commit changes](https://github.com/gisbi-kim/daily_arxiv_automation/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/gisbi-kim/daily_arxiv_automation/actions/workflows/main.yml)

# DARTA: Daily Arxiv Tracking Automation
## How to use?
1. on web: visit [https://arxiv-searcher.onrender.com](https://arxiv-searcher.onrender.com)
2. on your local machine: `git clone` and `sh run_app.sh`

![스크린샷 2023-03-19 01 52 08](https://user-images.githubusercontent.com/14989535/226121228-3b43a547-ff6f-4b27-b71c-1afbe088fe8e.png)

## Features 
### 1. Automatically parse a daily arxiv rss 
  - a. `python3 arxiv_saver_to_db.py`: parse information and save into the database (sqlite3)
    - This DB is automatically growing (appending) via Github Action.
    - example 
        - <img width="1481" alt="스크린샷 2023-03-18 20 03 42" src="https://user-images.githubusercontent.com/14989535/226101492-404c0196-98ad-4070-891b-81122175623f.png">
        - <img width="1052" alt="스크린샷 2023-03-18 20 02 41" src="https://user-images.githubusercontent.com/14989535/226101513-b6c166c8-2db2-4f3c-9332-d2986b34d9e6.png">
  - b. (optional) `python3 arxiv_saver_as_pdf.py`: download the all pdfs
    - with auto-naming as {YY} {Title}
    - example
      - <img width="488" alt="image" src="https://user-images.githubusercontent.com/14989535/221883912-90e6c89b-1b51-498a-b51b-969736575140.png">

### 2. Search web app
- Just do `run_app.sh` 
  - The dependencies: fastapi, uvicorn, and streamlit
- example 
  - The image of the top!

## Tips 
- To make a requirements.txt file, `pipreqs --encoding=utf8` would be helpful.

## TODO
- sqlite3 파일을 github repository (100mb 제한) 가 아닌 원격 저장소에서 pull해오고 push하기
