from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db import fetch_all_films, fetch_film_by_id

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000/*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Film(BaseModel):
    title: str
    film_id: int
    relative_url: str
    blu_ray: bool | None = None
    four_kay: bool | None = None


@app.get("/api/films")
def read_rood(page: int = 0, limit: int = 24):
    films = fetch_all_films(page, limit)
    if len(films) < 1:
        return {"result": "No films"}
    return films


@app.get("/api/films/{film_id}")
async def read_item(film_id: str):
    print(film_id)
    film = fetch_film_by_id(film_id)
    return film
