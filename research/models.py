import datetime
from dataclasses import dataclass


@dataclass
class Rating:
    user_id: str
    film_id: str
    rating: int
    date_created: datetime.datetime


@dataclass
class Review:
    user_id: str
    film_id: str
    text: str
    date_created: datetime.datetime


@dataclass
class Bookmark:
    user_id: str
    film_id: str
    date_created: datetime.datetime
