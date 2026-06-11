import json
from math import ceil

from fastapi import Query
from sqlmodel import Field, SQLModel, Session, col, create_engine, select, func


class Watchlist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    film_id: int
    relative_url: str
    blu_ray: bool | None = None
    four_kay: bool | None = None
    poster: str | None = None


class FilmCreate(SQLModel):
    title: str
    relative_url: str
    film_id: int


class FilmUpdate(SQLModel):
    title: str | None = None
    relative_url: str | None = None
    blu_ray: bool | None = None
    four_kay: bool | None = None
    poster: str | None = None


file_name = "watchlist.db"

url = f"sqlite:///{file_name}"

engine = create_engine(url, echo=True)


def db_init():
    SQLModel.metadata.create_all(engine)


def insert_film(data):
    json_data = json.dumps(data)
    with Session(engine) as session:
        valid = Watchlist.model_validate(json.loads(json_data))
        session.add(valid)
        session.commit()


def fetch_all_films(page: int = 1, limit: int = Query(default=24, le=24)):
    offset = (page - 1) * limit
    with Session(engine) as session:
        statement = select(Watchlist)
        res = session.exec(statement.offset(offset).limit(limit))
        count = session.exec(select(func.count(col(Watchlist.id)))).one()
        print("count one", count)
        print("count / limit", ceil(count / limit))
        return {"results": res.all(), "pages": ceil(count / limit), "current_page": page if page > 0 else 1}


def fetch_film_by_id(film_id: str):
    with Session(engine) as session:
        film = session.get(Watchlist, int(film_id))
        if not film:
            raise Exception("Film not found")

        return film


def update_film(film_id, data):
    json_data = json.dumps(data)
    with Session(engine) as session:
        film = session.get(Watchlist, film_id)
        if not film:
            raise Exception("Film not found")
        valid = FilmUpdate.model_validate(json.loads(json_data))
        new_data = valid.model_dump(exclude_none=True)

        film.sqlmodel_update(new_data)

        session.add(film)
        print(film)
        session.commit()


if __name__ == "__main__":
    db_init()
