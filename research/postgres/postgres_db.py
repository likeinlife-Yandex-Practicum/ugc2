import logging
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import execute_batch

from postgres.errors import DbError


class PostgresDb:

    def __init__(self, config: dict, batch_size: int = 100):
        self._logger = logging.getLogger(__name__)
        self._config = config
        self._batch_size = batch_size
        self._connection = None

    def __enter__(self, *args):
        self._connect()
        self._logger.info('Connect to postgres\n')
        return self

    def __exit__(self, *args):
        self._connection.close()
        self._logger.info('Connection closed')

    def _connect(self):
        self._connection = psycopg2.connect(dbname=self._config['DB_NAME'],
                                            user=self._config['DB_USER'],
                                            password=self._config['DB_PASSWORD'],
                                            host=self._config['DB_HOST'],
                                            port=self._config['DB_PORT'],
                                            options='-c search_path=public'
                                            )

    @contextmanager
    def _db_query(self, query, *args, **kwargs):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, *args, **kwargs)
            yield cursor
        except Exception as err:
            raise DbError(f'Exception of execute query: {query}\n{err}')
        finally:
            cursor.close()

    def batch_insert(self, query, args_list):
        cursor = self._connection.cursor()
        try:
            execute_batch(cursor, query, args_list, page_size=self._batch_size)
            self._connection.commit()
        except Exception as err:
            raise DbError(f'Exception of execute query: {query}\n{err}')
        finally:
            cursor.close()

    def _select(self, query, *args, fetch_one=False, **kwargs):
        with self._db_query(query, *args, **kwargs) as cursor:
            result = cursor.fetchone() if fetch_one else cursor.fetchall()
            return result

    def select_one(self, query, *args, **kwargs):
        result = self._select(query, *args, fetch_one=True, **kwargs)
        return result

    def select_all(self, query, *args, **kwargs):
        result = self._select(query, *args, fetch_one=False, **kwargs)
        return result

    def insert_many(self, query, args_list):
        cursor = self._connection.cursor()
        result = cursor.executemany(query, args_list)
        self._connection.commit()
        return result
