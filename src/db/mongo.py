from motor.core import AgnosticClient

from .errors import MongoClientNotInitializedError

mongo_client: None | AgnosticClient = None


def get_mongo_client() -> AgnosticClient:
    if mongo_client:
        return mongo_client
    raise MongoClientNotInitializedError
