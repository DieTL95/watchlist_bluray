from time import sleep

import bs4
import urllib3


def bluray_film_find(film_id, name):
    """
    Scrubs blu-ray.com film pages to find if the film has a Blu-ray or 4K release.
    First it calls fetch_film_by_name_search() with the film name.
    If an exact match exists with no overlapping films with the same title and year
    it will automatically redirect to the film's overview page with the info we need.
    If multiple exist, it will iterate over them and whichever one matches the name and year we want will get scrubbed.
    If none exist, it will return.

    When a film matches, it checks if there's a BR or 4K release, and updates the film in the database.
    """
    from db import update_film
    sleep(3)
    soup = fetch_film_by_name_search(name)

    title = soup.select_one("title")
    if title is None:
        print("No title")
        return
    if str(title.text).strip() == "Blu-ray.com - Search":
        print("Search")
        search_row = soup.find_all("div", attrs={"class": "figure"})
        if search_row is None:
            print("Film doesn't exist")
            return
        for row in search_row:
            a_tag = row.find("a")
            if a_tag is None:
                print("Film doesn't exist")
                return
            if str(a_tag.get("alt")).strip().lower() == name.strip().lower():
                href = a_tag.get("href")
                print(href)
                soup = fetch_film_by_name_search("", href)

    print(title)
    parent_div = soup.find("div", attrs={"id": "content_overview"})
    if parent_div is None:
        return
    content_div = parent_div.find_all("div", recursive=False)[2]

    releases_parent = content_div.find("div", recursive=False)
    if releases_parent is None:
        return

    releases = releases_parent.find("div", recursive=False)

    if releases is None:
        return

    for div in releases.find_all("div", recursive=False):

        if div.getText().lower().strip() == "blu-ray":
            update = update_film(str(film_id), {"blu_ray": True})
            print(f"Blu-ray found for: {name}")
            if update == "Update successful":
                print("Blu-ray added")
        if div.getText().lower().strip() == "4k blu-ray":
            update = update_film(str(film_id), {"four_kay": True})
            print(f"4K found for: {name}")
            if update == "Update successful":
                print("4k added")


def fetch_film_by_name_search(name, film_url=None):
    """
    Finds a film on blu-ray.com by name, if an exact match exists it will automatically redirect othe film's overview page.
    """

    url = f"https://www.blu-ray.com/search/?quicksearch=1&quicksearch_country=US&quicksearch_keyword={name}&section=theatrical" if film_url is None else film_url

    data = urllib3.request("GET", url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'})
    print(url)
    soup = bs4.BeautifulSoup(data.data)
    return soup
