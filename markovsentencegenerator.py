import requests
import pyperclip
import re
from urllib.error import HTTPError
from bs4 import BeautifulSoup


# Making sure user has a valid URL in clipboard.

while True:
    if (truth := input("Is the URL you intend to scrape in your clipboard? \ny / n\n")).lower() != 'y':
        continue
    else:
        break


# Grabbing user's URL from the
base_url = pyperclip.paste()


try:
    response = requests.get(base_url)

    # If the response was successful, no Exception will be raised.
    response.raise_for_status()

    # Using BeautifulSoup to parse the HTML contents of the provided URL.
    initial_soup = BeautifulSoup(response.content, 'html.parser')

    # Kill all script and style elements
    for script in initial_soup(["script", "style"]):
        script.extract()  # Rip it out

    # Grabbing only the text in the URL.
    contents = initial_soup.get_text()

    # Break into lines and remove leading and trailing space on each.
    lines = (line.strip() for line in contents.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # List containing every character/word on the website.
    print(list(chunks))

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")








