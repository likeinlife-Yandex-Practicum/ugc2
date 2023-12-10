import random
from dataclasses import fields, astuple
from data.fake_data import generate_bookmarks, generate_ratings, generate_reviews
from data.other import TABLE_MODEL
from postgres.postgres_db import PostgresDb
from postgres.script.sql_script import INSERT_TO_TABLE, LIKE_COUNT, AVG_RATING, BOOKMARKS

from settings import pg_settings
from utils import timeit


@timeit
def write_data(_db, table_name: str, data: list):
    model = TABLE_MODEL[table_name]
    column_names = [field.name for field in fields(model)]
    bind_values = ', '.join(['%s'] * len(column_names))
    column_names = ', '.join(column_names)
    query = INSERT_TO_TABLE.format(table_name=table_name, column_names=column_names, bind_values=bind_values)
    _db.insert_many(query, [astuple(item) for item in data])
    print(f'Write to table: {table_name.upper()}')


@timeit
def get_film_like_count(_db, _film_id: str):
    result = _db.select_all(LIKE_COUNT, (_film_id,))
    return result


@timeit
def get_average_rating(_db, _film_id: str):
    result = _db.select_one(AVG_RATING, (_film_id,))
    return result[0] if result else 0


@timeit
def get_user_bookmarks(_db, _user_id: str):
    result = _db.select_all(BOOKMARKS, (_user_id,))
    return result


if __name__ == '__main__':
    amount = 100

    postgres_settings = {
        'DB_HOST': pg_settings.host,
        'DB_PORT': pg_settings.port,
        'DB_NAME': pg_settings.db,
        'DB_USER': pg_settings.user,
        'DB_PASSWORD': pg_settings.password,
    }
    with PostgresDb(postgres_settings, batch_size=pg_settings.batch_size) as postgres_db:
        ratings = list(generate_ratings(amount))
        reviews = list(generate_reviews(amount))
        bookmarks = list(generate_bookmarks(amount))
        print('=========== write tests ==========')
        write_data(postgres_db, pg_settings.ratings_table, ratings)
        write_data(postgres_db, pg_settings.reviews_table, reviews)
        write_data(postgres_db, pg_settings.bookmarks_table, bookmarks)
        print('=========== read tests ==========')
        film_id = random.choice(ratings).film_id
        likes_count_result = get_film_like_count(postgres_db, film_id)
        average_rating = get_average_rating(postgres_db, film_id)
        user_id = random.choice(bookmarks).user_id
        user_bookmarks = get_user_bookmarks(postgres_db, user_id)
