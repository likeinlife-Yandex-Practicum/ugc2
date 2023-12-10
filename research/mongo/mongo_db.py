from dataclasses import asdict
import logging
import typing

from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.errors import PyMongoError

from settings import MongoSettings
from data.fake_data import generate_bookmarks, generate_ratings, generate_reviews


class MongoDb:

    def __init__(
            self,
            settings: MongoSettings,
            client: MongoClient | None = None,
    ) -> None:
        self._config = settings
        self._client = client
        self._logger = logging.getLogger(__name__)

    @property
    def mongo_conn(self) -> MongoClient | None:
        try:
            if self._client is None or not self._client.admin.command('ping'):
                self._client = self.create_client()
        except PyMongoError as err:
            self._logger.error('Mongo connection error: %s', err)
            return None
        return self._client

    def create_client(self) -> MongoClient:
        return MongoClient(
            self._config.mongo_connection_string,
        )

    def get_database(self) -> Database | None:
        if self.mongo_conn is None:
            return None
        return self.mongo_conn[self._config.db_name]

    @staticmethod
    def create_batch(
            iterable: typing.Iterator,
            batch_size: int,
    ) -> typing.Iterator[list]:
        batch = []
        for elem in iterable:
            batch.append(elem)
            if len(batch) % batch_size == 0:
                yield batch
                batch = []
        if batch:
            yield batch

    def clean_data(self) -> None:
        db = self.get_database()
        db[self._config.ratings_collection].drop()
        db[self._config.reviews_collection].drop()
        db[self._config.bookmarks_collection].drop()

    def create_collections(self) -> None:
        db = self.get_database()
        db.create_collection(self._config.ratings_collection)
        db[self._config.ratings_collection].create_index([('film_id', ASCENDING)])

        db.create_collection(self._config.reviews_collection)
        db[self._config.reviews_collection].create_index([('film_id', ASCENDING)])

        db.create_collection(self._config.bookmarks_collection)
        db[self._config.bookmarks_collection].create_index([('user_id', ASCENDING)])

    def insert_data(
            self,
            cn_name: str,
            cn_data: list[dict],
    ) -> None:
        database = self.get_database()
        if database is not None:
            database[cn_name].insert_many(cn_data)

    def get_collection_counts(self, cn_name: str) -> int | None:
        database = self.get_database()
        if database is not None:
            return database[cn_name].count_documents({})
        return None

    def add_ratings(self, amount: int) -> None:
        film_ratings = generate_ratings(amount)
        for count, batch in enumerate(
                self.create_batch(film_ratings, self._config.batch_size),
                start=1,
        ):
            self.insert_data(
                self._config.ratings_collection,
                [asdict(user_film_rating) for user_film_rating in batch],
            )
            self._logger.info(self._config.batch_size * count, 'rows inserted')

    def add_reviews(self, amount: int) -> None:
        reviews = generate_reviews(amount)
        for count, batch in enumerate(
                self.create_batch(reviews, self._config.batch_size),
                start=1,
        ):
            self.insert_data(
                self._config.reviews_collection,
                [asdict(review) for review in batch],
            )
            self._logger.info(self._config.batch_size * count, 'rows inserted')

    def add_bookmarks(self, amount: int) -> None:
        bookmarks = generate_bookmarks(amount)
        for count, batch in enumerate(
                self.create_batch(bookmarks, self._config.batch_size),
                start=1,
        ):
            self.insert_data(
                self._config.bookmarks_collection,
                [asdict(bookmark) for bookmark in batch],
            )
            self._logger.info(self._config.batch_size * count, 'rows inserted')

    def insert_many(self, cn_name: str, data: list[dict]) -> None:
        db = self.get_database()
        db[cn_name].insert_many(data)

    def count_likes(self) -> list[dict]:
        db = self.get_database()
        pipeline = [{'$group': {'_id': '$film_id', 'likes_count': {'$sum': 1}}}]
        result = db[self._config.ratings_collection].aggregate(pipeline)
        return list(result)

    def get_average_rating(self, film_id: str) -> float | int:
        db = self.get_database()
        pipeline = [
            {'$match': {'film_id': film_id}},
            {'$group': {'_id': None, 'average_rating': {'$avg': '$rating'}}},
        ]
        result = list(db[self._config.ratings_collection].aggregate(pipeline))
        return result[0]['average_rating'] if result else 0

    def get_user_bookmarks(self, user_id: str) -> list[dict]:
        db = self.get_database()
        collection = db[self._config.bookmarks_collection]
        result = collection.find({'user_id': user_id})
        return list(result)
