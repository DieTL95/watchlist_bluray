import os
from time import sleep
from dotenv import load_dotenv
import requests

from db import fetch_all_films, update_film

load_dotenv()


def fetch_poster(name, year):
    """
    Fetching film posters from TMDB using their API.
    Films are found by name and release year, first film is automatically chosen. 
    """
    tmb_token = os.getenv("TMDB_ACCESS_TOKEN")
    url = f"https://api.themoviedb.org/3/search/movie?query='{name}'&year={year}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmb_token}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    if data["total_results"] == 0:
        return None
    return data["results"][0]["poster_path"]


def add_films_posters():
    """
        Adding the above fetched film's poster url to the film's row in the database. 
        Ensuring film title and year match with the one we're adding the poster to.
        Using TMDB pre-resized urls with the relative path provided from the API call.
        (There is also an 'Original' quality and other resolutions but sticking with the width 500 for convience and speed.)
    """

    films = fetch_all_films()

    for film in films["results"]:
        if film.poster:
            continue
        if film.title.strip().endswith(")"):
            title = film.title[:-6].strip()
            year = film.title[-5:-1].strip()
            poster_path = fetch_poster(title, year)
            if not poster_path:
                continue
            else:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                update_film(film.id, {"poster": poster_url})
                sleep(1)
        else:
            print(film.title)


if __name__ == "__main__":
    add_films_posters()
