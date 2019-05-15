#!/usr/bin/env python3.6

import re
import os
import argparse
from downloader import Downloader


def valid_username(username):
    if 1 <= len(username) <= 30:
        pattern = "^[a-zA-Z0-9_][a-zA-Z0-9_.]+[a-zA-Z0-9_]$"
        match = re.match(pattern, username)
        return match

def main(username, max=1):
    user = os.path.join('https://www.instagram.com/', username)
    bot = Downloader()
    bot.open(user)
    urls = bot.get_urls(max)
    for url in urls:
        bot.download(url)
    bot.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Instagram username.")
    parser.add_argument("-l", "--limit", help="limit the number posts to download. Set it to 0 to download all posts.", type=int, default=1)
    args = parser.parse_args()

    if valid_username(args.username):
        main(args.username, args.limit)
