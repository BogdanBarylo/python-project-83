CREATE TABLE urls(
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
name varchar(255) NOT NULL UNIQUE,
created_at timestamp DEFAULT NOW()
);

CREATE TABLE url_checks(
id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
url_id bigint REFERENCES urls (id),
status_code integer,
h1 varchar(255),
title varchar(255),
description varchar,
created_at timestamp DEFAULT NOW()
);