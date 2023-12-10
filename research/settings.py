from pydantic import Field
from pydantic_settings import BaseSettings


class MongoSettings(BaseSettings):
    mongo_connection_string: str = Field('mongodb://localhost:27017')
    db_name: str = Field('test_db')
    batch_size: int = Field(10_000)
    ratings_collection: str = Field('ratings')
    reviews_collection: str = Field('reviews')
    bookmarks_collection: str = Field('bookmarks')


class PostgresSettings(BaseSettings):
    db: str = Field()
    user: str = Field()
    password: str = Field()
    host: str = Field()
    port: int = Field()

    batch_size: int = Field(10_000)
    ratings_table: str = Field('ratings')
    reviews_table: str = Field('reviews')
    bookmarks_table: str = Field('bookmarks')

    class Config:
        env_prefix = 'postgres_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


mongo_settings = MongoSettings()
pg_settings = PostgresSettings()
