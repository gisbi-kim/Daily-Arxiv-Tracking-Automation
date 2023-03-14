import sqlite3
import feedparser
import requests
import os
import datetime
import re


def batch_donwload(feed, directory, schema_name, conn, download_pdf=False):
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {schema_name} (title TEXT, year INTEGER, summary TEXT, link TEXT)")

    # Iterate over entries and download PDFs
    for entry in feed.entries:
        # parse meta data
        year = entry.id.split('/')[-1][:2]
        title = entry.title.split(
            '. (arXiv')[0].replace(':', ' - ').replace('/', '')
        summary = entry.summary.replace('<p>', '').replace(
            '</p>', '').replace('\n', '')

        filename = f"{year} {title}.pdf"
        filename = re.sub(r'[<>:"/\\|?*]', ' ', filename)
        filename = os.path.join('./', directory, filename)

        # Check if file already exists
        if os.path.isfile(filename):
            print(f"The file already exists. Skipping:\n  {filename}")
            continue

        # print info
        print(f"{year} {title}")
        print(f"  {summary}")
        print(filename)

        # download link
        link = (entry.link + '.pdf').replace('abs', 'pdf')
        print(f"\nlink: {link}")
        print(f" Requesting PDF for\n  {title}\n\n")

        # append to db
        cursor.execute(f"SELECT * FROM {schema_name} WHERE title=?", (title,))
        if not cursor.fetchone():
            datum_info = '(title, year, summary, link)'
            datum = (title, year, summary, link)
            cursor.execute(
                f"INSERT INTO {schema_name} {datum_info} VALUES (?, ?, ?, ?)", datum)

        conn.commit()

        # Download PDF and save to file
        if download_pdf:
            response = requests.get(link)
            with open(filename, 'wb') as f:
                f.write(response.content)


def batch_download_ID(id, save_id, conn, download_pdf):
    directory = f'arxiv_pdfs_{save_id}'
    if not os.path.exists(directory):
        os.mkdir(directory)

    feed_url = f'http://export.arxiv.org/rss/cs.{id}'
    feed = feedparser.parse(feed_url)
    print(f"{len(feed.entries)} items going to be loaded.")

    schema_name = id
    batch_donwload(feed, directory, schema_name, conn, download_pdf)


def main():
    conn = sqlite3.connect("arxiv_papers.db")

    download_pdf_list = [False]
    for download_pdf in download_pdf_list:
        batch_download_ID("RO", "ro", conn, download_pdf)
        batch_download_ID("CV", "cv", conn, download_pdf)
        batch_download_ID("AI", "ai", conn, download_pdf)
        batch_download_ID("LG", "lg", conn, download_pdf)
        batch_download_ID("GR", "gr", conn, download_pdf)

    conn.close()


main()
