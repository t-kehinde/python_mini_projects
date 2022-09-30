# #########################################################################
# TEXT BASED BROWSER
# tags: [web_scraping, HTTP requests, colored terminal text]
#
# This program extracts and saves the content of webpages in markdown format
# #########################################################################


import os
import sys

from collections import deque
import re
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def url_validation(tb_url: str) -> str:
    ''' Check that the user provided a valid url '''

    # prepend http to the url if it is missing
    http_verification = re.compile(
        r'^(?:http|ftp)s?://')  # http:// or https://
    tb_url = "http://" + \
        tb_url if http_verification.search(tb_url) is None else tb_url

    # verify that a valid page connects to the server
    is_valid_url = re.compile(
        r'(^https?:\/\/)?(www\.)?\w+\.(com|org|gov|io)')
    if is_valid_url.search(tb_url) is None:
        print("incorrect URL")
        return "invalid"
    try:
        response = requests.get(tb_url)
        if not response:
            raise ConnectionError
    except ConnectionError:
        print("Connection Error: incorrect URL")
        return "invalid"


def web_scrape(url_page: str):
    '''Extract the text from the url page'''
    # Make HTTP GET request
    response = requests.get(url_page)
    page_content = response.content
    # Use beautiful soup to parse the html and read page body
    soup = BeautifulSoup(markup=page_content,
                         features="html.parser", from_encoding="UTF-8")
    # Get the links from page
    links = []
    for link in soup.find_all('a'):
        if len(link.get_text(strip=True)) != 0:
            links.append(link.get_text(" ", strip=True))
    # Get the text from the entire page
    html = []
    for html_tag in soup.find_all():
        if len(html_tag.get_text(strip=True)) != 0 and \
            html_tag.name not in ['header'] and \
                html_tag.name in ['p', 'a', 'ul', 'ol',  'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            html.append(html_tag.get_text(" ", strip=True))

    for phrase in html:
        if phrase in set(links):
            print(Fore.BLUE + phrase)
        else:
            print(Fore.BLACK + phrase)
    return " ".join(html)                   # returns page content


def url_tabs(user_input: str, directory: str) -> None:
    ''' Save the webpage ( url ) to the directory and print to stdout '''
    news_queue = deque()                    # create a queue to store tabs
    pages_removed_from_queue = []           # storage for the popped items

    while user_input != "exit":
        # Simulate the back button on a browser with a "back" command. Note
        # that a prompt right after the addition of a url is analogous to the
        # current page in a browser. The url before the last saved is the
        # previous page.
        if user_input == "back":
            if len(news_queue) < 2:         # return to previous url if any
                pass
            else:
                prev_saved_page = news_queue.pop()
                pages_removed_from_queue.append(prev_saved_page)
                prev_saved_page = news_queue.pop()
                # print the previous page
                print(prev_saved_page)
                pages_removed_from_queue.append(prev_saved_page)
        else:
            for _ in range(len(pages_removed_from_queue)):
                news_queue.append(pages_removed_from_queue.pop())
            # verify that the url is valid
            validate_url = url_validation(user_input)
            while validate_url == "invalid":
                user_input = input()
                if user_input == "exit" or user_input == "back":
                    break                     # exit validation
                validate_url = url_validation(user_input)

            # The inner loop to validate the url is not executed if the user
            # enters "exit" or "back" command. So, the conditions for these
            # commands are restored outside the while loop.
            if user_input == "exit":
                break
            if user_input == "back":
                continue

            # Prepend http to the url if it is missing
            if user_input.startswith("http://"):
                url = user_input
            else:
                url = "http://" + user_input
            # Add verified url tab to the queue
            news_queue.append(url)
            page_text = web_scrape(url)      # extract the text from the page
            print(page_text)                 # print the text to stdout
            # save page content to file
            filename = url[7:].rpartition(".")[0].replace(".", "_")
            with open(directory + "/" + filename, "w",
                      encoding='UTF-8') as text_file:
                text_file.write(page_text)
            # task complete message
            print(f"Page saved to file {filename}")
        # Prompt the user to enter a new url
        user_input = input()


# =============================================================================
# Create a directory to save the news articles
args = sys.argv         # list of arguments from the command line
news_dir = args[1]      # prompt for directory to save the urls
try:
    os.mkdir(news_dir)
    print("Directory created.")
except FileExistsError:
    print("Directory already exists.")
# call the function to save the webpage to the directory
tabs_input = input()
url_tabs(tabs_input, news_dir)
