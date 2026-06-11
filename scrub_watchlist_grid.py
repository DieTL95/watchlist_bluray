import json
import mechanicalsoup


def get_films(url):
    """
    Scrubbing the provided Letterboxd watchlist page films using MechanicalSoup and adds them to the database.
    """

    browser = mechanicalsoup.StatefulBrowser(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36")
    browser.open(url)
    films = []

    grid_items = browser.page.find_all(
        "li", attrs={"class": "griditem"}) if browser.page is not None else []
    for thing in grid_items:
        film = dict()
        child = thing.find("div")
        if child:
            name = child.get("data-item-full-display-name")
            relative_url = child.get("data-item-link")
            poster_attr = child.get('data-resolvable-poster-path')

            film_uid = json.loads(str(poster_attr))[
                "postered"]["uid"].split(":")[-1]
            film["title"] = name
            film["relative_url"] = relative_url
            film["id"] = film_uid
        films.append(film)
    browser.close()
    return films
