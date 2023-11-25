#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER bogdan WITH PASSWORD 'pass';
    CREATE DATABASE db_analyzer;
    GRANT ALL PRIVILEGES ON DATABASE db_analyzer TO bogdan;
    CREATE TABLE urls (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT NOW()
    );
EOSQL