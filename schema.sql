CREATE TABLE Users (
    user_id SERIAL,
    username TEXT UNIQUE,
    password TEXT,
    isadmin BOOLEAN,
    PRIMARY KEY (user_id)
);