CREATE TABLE Users (
    user_id SERIAL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    isadmin BOOLEAN,
    PRIMARY KEY (user_id)
);

CREATE TABLE events (
    event_id SERIAL,
    event_name TEXT UNIQUE NOT NULL,
    event_description TEXT,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    ispublic BOOLEAN,
    user_id INTEGER REFERENCES Users,
    PRIMARY KEY (event_id)
);