import feedparser
import requests
import os
import datetime
import re 

def batch_donwload(feed, directory):
    # Iterate over entries and download PDFs
    for entry in feed.entries:
        # parse meta data 
        year = entry.id.split('/')[-1][:2]
        title = entry.title.split('. (arXiv')[0].replace(':', ' - ').replace('/', '')
        summary = entry.summary.replace('<p>', '').replace('</p>', '').replace('\n', '')

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

        # download 
        link = (entry.link + '.pdf').replace('abs', 'pdf')
        print(f"\nlink: {link}")
        print(f" Requesting PDF for\n  {title}\n\n")
        
        # Download PDF and save to file
        response = requests.get(link)
        with open(filename, 'wb') as f:
            f.write(response.content)


def batch_download_ID(id, save_id):
    directory = f'arxiv_pdfs_{save_id}'
    if not os.path.exists(directory):
        os.mkdir(directory)

    feed_url = f'http://export.arxiv.org/rss/cs.{id}'
    feed = feedparser.parse(feed_url)
    print(f"{len(feed.entries)} items going to be loaded.")
    batch_donwload(feed, directory)

def main():
    batch_download_ID("AI", "ai")
    batch_download_ID("RO", "ro")
    batch_download_ID("CV", "cv")
    batch_download_ID("GR", "gr")

main()