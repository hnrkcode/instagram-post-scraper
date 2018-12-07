#!/usr/bin/env python3.6

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.options import Options


class WebDriver:
    """Responsible for starting and closing Selenium."""

    def __init__(self):
        """Initialize headless mode by default."""
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)

    def open(self, url):
        """Open the url in the webdriver."""
        try:
            self.driver.get(url)
        except exceptions.WebDriverException:
            self.close()

    def close(self):
        """Close the web driver."""
        self.driver.close()
