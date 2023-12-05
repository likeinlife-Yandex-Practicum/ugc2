from beanie import Document

from .common import HasTimeStamp, HasUserId, HasUUIDId


class MongoBaseDocument(HasTimeStamp, HasUserId, HasUUIDId, Document):
    ...
