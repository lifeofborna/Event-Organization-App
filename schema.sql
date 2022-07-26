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

CREATE TABLE participant (
    participant_id SERIAL,
    user_id INTEGER REFERENCES Users,
    event_id INTEGER REFERENCES Events,
    PRIMARY KEY (participant_id)
);

CREATE TABLE comments (
    comment_id SERIAL,
    content TEXT,
    user_id INTEGER REFERENCES Users,
    event_id INTEGER REFERENCES Events,
    sent_at TIMESTAMP NOT NULL,
    PRIMARY KEY (comment_id)
);

CREATE TABLE invited (
    user_id INTEGER,
    event_id INTEGER,
    PRIMARY KEY(user_id,event_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);