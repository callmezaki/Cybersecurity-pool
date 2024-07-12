import requests as req
from bs4 import BeautifulSoup
import urllib.parse
import signal
import urllib.robotparser
import sys
import os

allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
visited_urls = set()
recursive_mode = False

def handle_html(base_url):
    response = req.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    img_urls = [urllib.parse.urljoin(base_url, img['src']) for img in soup.find_all('img', src=True)]
    page_urls = [urllib.parse.urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    return img_urls, page_urls

def download_image(url, path):
    file_extension = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if file_extension not in allowed_extensions:
        return
    
    response = req.get(url)
    file_name = os.path.join(path, os.path.basename(urllib.parse.urlparse(url).path))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f'Downloaded {file_name}')

def spider(url, path, depth, current_level=0):
    if current_level > depth or url in visited_urls:
        return

    visited_urls.add(url)
    img_urls, page_urls = handle_html(url)
    
    for img_url in img_urls:
        download_image(img_url, path)
    
    if not recursive_mode:
        return
    for page_url in page_urls:
        spider(page_url, path, depth, current_level + 1)

def signal_handler(sig, frame):
    print("\nInterrupted by user. Exiting gracefully.")
    sys.exit(0)

def handle_args(args):
    global recursive_mode  # Add this line to modify the global variable
    if args is None:
        print("Usage : spider.py [-rlhp] URL")
        exit()
    if "-r" in args:
        print("Recursive mode")
        recursive_mode = True

def main():
    args = sys.argv[1:]
    handle_args(args)
    # if len(args) != 1:
    #     print("Usage : spider.py URL")
    #     exit()

    url = args[0]
    path = 'images'
    rp = urllib.robotparser.RobotFileParser()
    signal.signal(signal.SIGINT, signal_handler)
    try:
        res = req.get(url)
        if res.status_code != 200:
            print("I got this code " + str(res.status_code) + " instead of 200")
            exit()

        read = req.get(urllib.parse.urljoin(url, '/robots.txt'))
        rp.parse(read.text.splitlines())
        if not rp.can_fetch("*", url):
            print(f"Fetching not allowed by robots.txt for {url}")
            exit()

        print("scraping ...")
        spider(url, path, 5)

    except req.exceptions.RequestException as e:
        print(f'Request failed: {e}')

if __name__ == '__main__':
    main()
