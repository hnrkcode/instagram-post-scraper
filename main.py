#!/usr/bin/env python3.6

from downloader import Downloader

if __name__ == "__main__":

    user = "https://www.instagram.com/instagram/"
    bot = Downloader()
    bot.open(user)
    urls = bot.get_urls(3)
    for url in urls:
        bot.download(url)
    bot.close()
