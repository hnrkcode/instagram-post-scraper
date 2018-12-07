#!/usr/bin/env python3.6

import re
import argparse
from downloader import Downloader

def valid_url(url):
    pattern = "https://www.instagram.com/[a-zA-Z0-9_]+/?"
    match = re.match(pattern, url)
    print(url, match)
    return match

def main(url, max=0):
    user = url
    bot = Downloader()
    bot.open(user)
    urls = bot.get_urls(max)
    for url in urls:
        bot.download(url)
    bot.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url to an instagram user.")
    parser.add_argument("-l", "--limit", help="limit the number posts to download.", type=int)
    args = parser.parse_args()

    if valid_url(args.url):
        if args.limit:
            main(args.url, args.limit)
        else:
            main(args.url)
