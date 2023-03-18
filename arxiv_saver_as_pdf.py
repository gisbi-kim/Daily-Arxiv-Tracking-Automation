import sqlite3
import feedparser
import requests
import os
import datetime
import re


def batch_donwload(feed, directory, schema_name, conn, download_pdf=False):
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
            print(f"The file already exists. Skip the paper\n   {filename}\n")
            continue

        # print info
        print(f"{year} {title}")
        print(f"  {summary}")
        print(filename)

        # download link
        link = (entry.link + '.pdf').replace('abs', 'pdf')
        print(f"\nlink: {link}")
        print(f" Requesting PDF for\n  {title}\n\n")

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
    conn = None
    batch_download_ID("RO", "ro", conn, True)
    batch_download_ID("CV", "cv", conn, True)
    batch_download_ID("AI", "ai", conn, True)
    batch_download_ID("LG", "lg", conn, True)
    batch_download_ID("GR", "gr", conn, True)


main()
