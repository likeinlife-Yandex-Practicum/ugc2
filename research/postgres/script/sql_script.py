from settings import pg_settings

INSERT_TO_TABLE = 'INSERT INTO {table_name} ({column_names}) VALUES ({bind_values})'

LIKE_COUNT = f'SELECT film_id, COUNT(*) FROM {pg_settings.ratings_table} WHERE film_id = %s GROUP BY film_id'
AVG_RATING = f'SELECT AVG(rating) FROM {pg_settings.ratings_table} WHERE film_id = %s'
BOOKMARKS = f'SELECT * FROM {pg_settings.bookmarks_table} WHERE user_id = %s'
