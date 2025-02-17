CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE user_games(
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    timestamp DATETIME,
    rating INTEGER DEFAULT NULL,
    commentary TEXT DEFAULT 'No comments'
);

CREATE TABLE games(
    id INTEGER NOT NULL,
    rating FLOAT,
    rating_count INTEGER
);
