import os
from time import sleep

import bs4
from dotenv import load_dotenv
import requests

from scrub_watchlist_grid import get_films
load_dotenv()

"""
Scrubbing a user's entire watchlist when provided with the first page.
Iterates over every watchlist page, passing the pages to the get_films() function which then scrubs the actual films and adds them to the database.
"""


url = os.getenv("WATCHLIST_URL")

if url is None:
    raise Exception("No URL Inserted.")

r = requests.get(url, headers={
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})

soup = bs4.BeautifulSoup(r.content, "html.parser")

next_page = soup.find_all("li", attrs={"class": "paginate-page"})
if next_page is None:
    raise Exception


all_films = []
print(next_page)
for link in range(1, int(next_page[-1].text) + 1):
    sleep(10)
    page_url = f"{url}page/{link}/"
    films = get_films(page_url)
    print(films)
    all_films.extend(films)
