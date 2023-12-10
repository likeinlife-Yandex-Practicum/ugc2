from models import Rating, Review, Bookmark
from settings import pg_settings

TABLE_MODEL = {
    pg_settings.ratings_table: Rating,
    pg_settings.reviews_table: Review,
    pg_settings.bookmarks_table: Bookmark,
}
