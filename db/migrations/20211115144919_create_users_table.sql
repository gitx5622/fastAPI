-- migrate:up
CREATE table users (
    id      BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
-- migrate:down
DROP TABLE users;

