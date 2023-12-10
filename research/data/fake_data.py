from data.data_helper import data_helper
from models import Rating, Review, Bookmark


def generate_ratings(count: int):
    for _ in range(count):
        yield Rating(
            user_id=data_helper.get_guid(),
            film_id=data_helper.get_guid(),
            rating=data_helper.get_random_int(),
            date_created=data_helper.get_random_datetime(),
        )


def generate_reviews(count: int):
    for _ in range(count):
        yield Review(
            user_id=data_helper.get_guid(),
            film_id=data_helper.get_guid(),
            text=data_helper.get_random_sentence(),
            date_created=data_helper.get_random_datetime(),
        )


def generate_bookmarks(count: int):
    for _ in range(count):
        yield Bookmark(
            user_id=data_helper.get_guid(),
            film_id=data_helper.get_guid(),
            date_created=data_helper.get_random_datetime(),
        )
