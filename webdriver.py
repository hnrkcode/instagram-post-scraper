#!/usr/bin/env python3.6

import sys
import os.path
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options


class WebDriver:
    """Responsible for starting and closing Selenium."""

    def __init__(self):
        """Initialize headless mode by default."""
        options = Options()
        options.add_argument("--headless")
        try:
            self.driver = webdriver.Firefox(
                firefox_options=options,
                executable_path=os.path.join(os.path.dirname(__file__), 'geckodriver')
            )
        except exceptions.WebDriverException as e:
            sys.exit(e)

    def open(self, url):
        """Open the url in the webdriver."""
        try:
            self.driver.get(url)
        except exceptions.WebDriverException:
            self.close()

    def close(self):
        """Close the web driver."""
        self.driver.close()
