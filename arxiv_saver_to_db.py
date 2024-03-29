import sqlite3
import feedparser
import requests
import os
import datetime
import re


def batch_donwload(feed, directory, schema_name, conn, download_pdf=False):
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {schema_name} (title TEXT, year INTEGER, summary TEXT, link TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

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

        # print info
        print(f"{year} {title}")
        print(f"  {summary}")
        print(filename)

        # download link
        link = (entry.link + '.pdf').replace('abs', 'pdf')
        print(f"\nlink: {link}")
        print(f" Requesting PDF for\n  {title}\n\n")

        # append to db
        try:
            cursor.execute(f"PRAGMA table_info({schema_name})")
            columns = [col[1] for col in cursor.fetchall()]
            if 'created_at' not in columns:
                cursor.execute(
                    f"ALTER TABLE {schema_name} ADD COLUMN created_at TIMESTAMP")

            cursor.execute(
                f"SELECT * FROM {schema_name} WHERE title=?", (title,))
            if not cursor.fetchone():
                datum_info = '(title, year, summary, link, created_at)'
                datum = (title, year, summary, link, datetime.datetime.now())
                cursor.execute(
                    f"INSERT INTO {schema_name} {datum_info} VALUES (?, ?, ?, ?, ?)", datum)
            else:
                datum_info = '(title, year, summary, link, created_at)'
                datum = (title, year, summary, link, datetime.datetime.now())
                cursor.execute(
                    f"UPDATE \"{schema_name}\" SET {datum_info} = (?, ?, ?, ?, ?) WHERE title = '{title}'",
                    datum
                )

            conn.commit()
        except:
            pass


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
    conn = sqlite3.connect("arxiv_papers.sqlite3")

    db_size = os.path.getsize("arxiv_papers.sqlite3")/(1024*1024)
    date = datetime.datetime.now().strftime('%Y-%m-%d')

    # 100mb under (because github allows a single file up to 100mb)
    if db_size > 99:
        os.rename("arxiv_papers.sqlite3", f"arxiv_papers_upto_{date}.sqlite3")
        conn = sqlite3.connect("arxiv_papers.sqlite3")
    else:
        conn = sqlite3.connect("arxiv_papers.sqlite3")

    batch_download_ID("RO", "ro", conn, False)
    batch_download_ID("CV", "cv", conn, False)
    batch_download_ID("AI", "ai", conn, False)
    batch_download_ID("LG", "lg", conn, False)
    batch_download_ID("GR", "gr", conn, False)

    conn.close()


main()
