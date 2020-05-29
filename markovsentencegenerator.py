import requests
import pyperclip
import re
import collections
import random
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
    tertiary_text = list((phrase.strip() for line in lines for phrase in line.split("  ")))

    # Regex file to only hold characters between a-zA-Z
    characters = re.compile('[a-zA-Z]')


    def punctuation_strip(lst):
        stripped_punctuation_list = []
        for item in lst:
            if characters.findall(item):
                stripped_punctuation_list.append(item)
            else:
                continue
        return stripped_punctuation_list


    secondary_text = punctuation_strip(tertiary_text)


    # Final list containing every single word from the provided URL.
    def convert(provided_list):
        primary_list = []
        temporary_text = []
        for sentence in provided_list:
            temporary_list = sentence.split()
            for word in temporary_list:
                primary_list.append(word)
        return primary_list


    primary_preliminary_list = convert(secondary_text)
    primary_text = punctuation_strip(primary_preliminary_list)
    print(primary_text)

    # Constructing probability matrix - Part 1.
    words = collections.Counter(primary_text)
    total_n_words = len(primary_text)

    # Creating a function to check if first letter is uppercase in a randomly selected dictionary
    def is_uppercase(word_dict):
        while True:
            if (a := random.choice(primary_text))[0].isupper():
                break
            else:
                continue
        return a

    lead_word = is_uppercase(words)
    print(lead_word)

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")

# https://en.wikipedia.org/wiki/Markov_chain
