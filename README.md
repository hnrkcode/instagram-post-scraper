# Instagram Post Scraper

Download Instagram posts from a specific user from the command line.

## Usage

Download the latest version of the [geckodriver](https://github.com/mozilla/geckodriver/releases) for your system and put it in the same directory as the script.

Then all you have to do is copy an url to an Instagram user and optionally specify how many posts you want to download. By default it only downloads the latest post.

**Downloads the latest post:**
`python3 main.py https://www.instagram.com/instagram/`

**Downloads the 23 latest post:**
`python3 main.py -l 23 https://www.instagram.com/instagram/`

**Downloads the all post:**
`python3 main.py -l 0 https://www.instagram.com/instagram/`
