CREATE TABLE IF NOT EXISTS ratings
(
    user_id      UUID PRIMARY KEY,
    film_id      UUID,
    rating       SMALLINT,
    date_created TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews
(
    user_id      UUID PRIMARY KEY,
    film_id      UUID,
    text         TEXT,
    date_created TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookmarks
(
    user_id      UUID PRIMARY KEY,
    film_id      UUID,
    date_created TIMESTAMP
);