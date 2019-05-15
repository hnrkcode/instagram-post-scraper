#!/usr/bin/env python3.6

import re
import os
import urllib
from . import settings
from urllib import request
from .scraper import Scraper
from bs4 import BeautifulSoup
from selenium.common import exceptions


class Downloader(Scraper):
    """Download files to the disk."""

    def __init__(self):
        super().__init__()
        self.output = "downloads"

    def get_extension(self, url):
        """Get the file extension of the file."""
        # Remove query string from the files url.
        clean_url = re.sub("([?].+)", "", url)
        file_ext = clean_url[-3:]
        return file_ext

    def post_type(self, url):
        """Check if it's multiple files in a single post."""
        try:
            multi_post = self.driver.find_element_by_class_name(settings.MULTI_POST)
        except exceptions.NoSuchElementException:
            multi_post = False

        if multi_post:
            return True
        else:
            return False  # Single post.

    def check_file_ext(self):
        """Checks if the element contains a video or an image file."""
        # Try if it's a video.
        try:
            element = self.driver.find_element_by_class_name(settings.VID_POST)
        except exceptions.NoSuchElementException as err:
            element = False
        # Try if it's an image.
        if not element:
            try:
                element = self.driver.find_element_by_class_name(settings.IMG_POST)
            except exceptions.NoSuchElementException as err:
                self.close()

        return element

    def multiple_files(self):
        """Post with multiple video or image files."""

        element = self.driver.find_element_by_class_name(settings.MULTI_FILES)
        element = element.get_attribute("innerHTML")
        soup = BeautifulSoup(element, 'html.parser')
        list_items = soup.find_all("li")

        # Total clicks is always two under the number of files in the post.
        # But subtract one instead of two in case there is only 2 files.
        clicks = len(list_items) - 1
        urls = []

        # Click next until all file urls in the post are scraped.
        for click in range(clicks):
            self.driver.find_element_by_class_name(settings.NEXT_BUTTON).click()
            innerHTML = self.driver.find_element_by_class_name(settings.MULTI_FILES)
            innerHTML = innerHTML.get_attribute("innerHTML")
            soup = BeautifulSoup(innerHTML, 'html.parser')

            for li in soup.find_all("li"):
                # Check if it's a video file, otherwise it's an image.
                if li.find("video"):
                    url = li.find("video")["src"]
                    if url not in urls:
                        urls.append(li.find("video")["src"])
                else:
                    if li.find("img"):
                        url = li.find("img")["src"]
                        if url not in urls:
                            urls.append(li.find("img")["src"])
        return urls

    def single_file(self):
        """Posts with only a single video or image file."""
        element = self.check_file_ext()
        file_url = [element.get_attribute("src")]
        return file_url

    def get_files(self, url):
        """Return all urls to the files to download."""
        multi_post = self.post_type(url)
        if multi_post:
            return self.multiple_files()
        else:
            return self.single_file()

    def create_filename(self):
        """Get the user that posted the post."""
        innerHTML = self.driver.page_source
        soup = BeautifulSoup(innerHTML, 'html.parser')
        username = soup.find(class_=settings.USERNAME).text
        data = soup.find_all(class_="_1o9PC Nzb55")[0]['datetime']
        data = re.sub("[\WTZ]", "", data)
        return username + data + str(id(data))

    def download(self, url):
        """Download the files."""
        self.open(url)  # Open the webdriver.
        files = self.get_files(url)

        for file in files:
            try:
                req = request.urlopen(file)
                name = self.create_filename()
                ext = self.get_extension(file)
            except (urllib.error.HTTPError, ValueError):
                self.close()
            else:
                file = req.read()
                # Create output folder if it doesn't exist.
                if not os.path.isdir(self.output):
                    os.mkdir(self.output)
                path = os.path.join(self.output, f"{name}.{ext}")
                # Download the file.
                with open(path, 'wb') as output:
                    print(f"Downloading {name}.{ext} to disk...")
                    output.write(file)
