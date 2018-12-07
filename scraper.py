#!/usr/bin/env python3.6

import time
import settings
from webdriver import WebDriver
from bs4 import BeautifulSoup


class Scraper(WebDriver):
    """Collect urls to posts that should be downloaded."""

    def __init__(self):
        super().__init__()

    def get_urls(self, max=0):
        """Collects urls to a users every post by default."""

        main = self.driver.find_element_by_class_name(settings.MAIN_CONTENT)
        innerHTML = main.get_attribute("innerHTML")
        soup = BeautifulSoup(innerHTML, 'html.parser')
        posts = soup.find_all(class_=settings.POST)
        scroll_pos = 0
        urls = set()

        # Will only get post urls up til the number of max's value.
        if max:
            total_posts = max
        # Will scrape every post url posted by the user by default.
        else:
            total_posts = int(soup.find_all(class_=settings.TOTAL_POSTS)[0].text)

        # Scroll down.
        while len(urls) < total_posts:
            # Limit the number of post urls to get to what 'total_posts' is.
            for post in posts[:total_posts]:
                url = "https://www.instagram.com" + post.parent['href']
                urls.add(url)

            main = self.driver.find_element_by_class_name(settings.MAIN_CONTENT)
            innerHTML = main.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, 'html.parser')
            posts = soup.find_all(class_=settings.POST)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_pos});")
            time.sleep(1)
            scroll_pos += 200

        return urls
