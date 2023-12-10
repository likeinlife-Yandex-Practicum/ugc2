from mongo.mongo_db import MongoDb
from settings import mongo_settings

if __name__ == '__main__':

    amount = 10 * 1_000_000

    mongo_db = MongoDb(settings=mongo_settings)
    mongo_db.clean_data()
    mongo_db.create_collections()

    collections = [
        (mongo_db.add_ratings, mongo_settings.ratings_collection),
        (mongo_db.add_reviews, mongo_settings.reviews_collection),
        (mongo_db.add_bookmarks, mongo_settings.bookmarks_collection),
    ]

    for insert_func, collection_name in collections:
        insert_func(amount)
        _amount = mongo_db.get_collection_counts(collection_name)
        print(f'Collection "{collection_name}" is done! element amount: {_amount}')
