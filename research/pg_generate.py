from dataclasses import astuple, fields
from typing import Generator

from data.fake_data import generate_ratings, generate_reviews, generate_bookmarks
from data.other import TABLE_MODEL
from postgres.postgres_db import PostgresDb
from postgres.script.sql_script import INSERT_TO_TABLE
from settings import pg_settings


def save_data_to_table(_db: PostgresDb, table_name: str, data: Generator):
    model = TABLE_MODEL[table_name]
    column_names = [field.name for field in fields(model)]
    bind_values = ', '.join(['%s'] * len(column_names))
    column_names = ', '.join(column_names)
    query = INSERT_TO_TABLE.format(table_name=table_name, column_names=column_names, bind_values=bind_values)
    _db.batch_insert(query, [astuple(item) for item in data])


if __name__ == '__main__':
    postgres_settings = {
        'DB_HOST': pg_settings.host,
        'DB_PORT': pg_settings.port,
        'DB_NAME': pg_settings.db,
        'DB_USER': pg_settings.user,
        'DB_PASSWORD': pg_settings.password,
    }
    with PostgresDb(postgres_settings, batch_size=pg_settings.batch_size) as postgres_db:
        amount = 10 * 1_000_000
        ratings = generate_ratings(amount)
        save_data_to_table(postgres_db, pg_settings.ratings_table, ratings)
        print(f'Table "{pg_settings.ratings_table}" is done!')

        reviews = generate_reviews(amount)
        save_data_to_table(postgres_db, pg_settings.reviews_table, reviews)
        print(f'Table "{pg_settings.reviews_table}" is done!')

        bookmarks = generate_bookmarks(amount)
        save_data_to_table(postgres_db, pg_settings.bookmarks_table, bookmarks)
        print(f'Table "{pg_settings.bookmarks_table}" is done!')
