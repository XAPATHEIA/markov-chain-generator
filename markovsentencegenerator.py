import requests
import pyperclip
import collections
import random
import string
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# Making sure user has a valid URL in clipboard.
while True:
    if (truth := input("Is the URL you intend to scrape in your clipboard? \ny / n\n")).lower() != 'y':
        continue
    else:
        break

try:
    # Grabbing user's URL from the
    base_url = pyperclip.paste()

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

    def punctuation_strip(lst):
        stripped_punctuation_list = []
        for item in lst:
            stripped_punctuation_list.append(item.strip(string.punctuation))
        return stripped_punctuation_list

    secondary_text = punctuation_strip(tertiary_text)

    # Final list containing every single word from the provided URL.
    def convert(provided_list):
        primary_list = []
        temporary_list = []
        for sentence in provided_list:
            temporary_list = sentence.split()
            for word in temporary_list:
                primary_list.append(word)
        return primary_list


    while True:
        if (n_of_sentences := int(input("How many sentences would you like to generate? (More usually means you will "
                                        "get a coherent sentence eventually). \n"))) <= 0:
            continue
        else:
            break

    for renewal in range(n_of_sentences):
        primary_preliminary_list = convert(secondary_text)
        primary_text = []
        for item in primary_preliminary_list:
            primary_text.append(item.strip(string.punctuation))

        # Creating a set in order to remove duplicates so as to allow for reliable root word selection.
        unique_set = set(primary_text)

        # Randomly selecting initial root word so as to allow diversity in generated sentences.
        root_word = random.choice(tuple(unique_set))

        generated_sentence = root_word.capitalize()

        random_sentence_length = random.randint(5, 20)

        for iteration in range(random_sentence_length):
            # Locating the index of the words that come AFTER the root word.
            indices = [i + 1 for i, x in enumerate(primary_text) if x == root_word]

            # Turning the indices into strings so that they can be counted.
            following_words_raw = []
            if not indices:
                print("Nothing in here")
                break
            for k in indices:
                following_words_raw.append(primary_text[k])

            # Constructing probability distribution.
            probability_distribution = []
            u_following_words = list(set(following_words_raw))
            for word in u_following_words:
                probability_distribution.append(round(following_words_raw.count(word) / len(following_words_raw), 10))

            if not probability_distribution:
                print(generated_sentence + ".")
                break
            elif len(probability_distribution) == 1:
                root_word = u_following_words[0]
            else:
                root_word = random.choices(
                    population=u_following_words,
                    weights=probability_distribution,
                    k=1)
                root_word = root_word[0]

            a = root_word
            if not a:
                print(generated_sentence + ".")
                break
            elif iteration == random_sentence_length:
                generated_sentence += " " + a + "."
                break
            else:
                generated_sentence += " " + a

        print(generated_sentence + ".")

except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")
