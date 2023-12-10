from dataclasses import asdict
import random

from mongo.mongo_db import MongoDb
from settings import mongo_settings
from data.fake_data import generate_bookmarks, generate_ratings, generate_reviews
from utils import timeit


@timeit
def write_data(mongo_db: MongoDb, collection_name, data):
    mongo_db.insert_many(collection_name, data)


@timeit
def get_film_like_count(mongo_db: MongoDb):
    return mongo_db.count_likes()


@timeit
def get_average_rating(mongo_db: MongoDb, film_id: str):
    result = mongo_db.get_average_rating(film_id)
    return result


@timeit
def get_user_bookmarks(mongo_db: MongoDb, user_id: str):
    result = mongo_db.get_user_bookmarks(user_id)
    return result


if __name__ == '__main__':
    amount = 10

    _mongo_db = MongoDb(settings=mongo_settings)

    ratings = list(generate_ratings(amount))
    reviews = list(generate_reviews(amount))
    bookmarks = list(generate_bookmarks(amount))

    user_film_ratings_dicts = [asdict(item) for item in ratings]
    reviews_dicts = [asdict(item) for item in reviews]
    bookmarks_dicts = [asdict(item) for item in bookmarks]
    print('=========== write tests ==========')
    write_data(_mongo_db, mongo_settings.ratings_collection, user_film_ratings_dicts)
    write_data(_mongo_db, mongo_settings.reviews_collection, reviews_dicts)
    write_data(_mongo_db, mongo_settings.bookmarks_collection, bookmarks_dicts)
    print('=========== read tests ==========')
    likes_count_result = get_film_like_count(_mongo_db)
    film_id = random.choice(ratings).film_id
    average_rating = get_average_rating(_mongo_db, film_id)
    user_id = random.choice(bookmarks).user_id
    user_bookmarks = get_user_bookmarks(_mongo_db, user_id)
