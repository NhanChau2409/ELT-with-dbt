CREATE SCHEMA IF NOT EXISTS sources;

CREATE TABLE IF NOT EXISTS sources.helsinki (
    from_date TIMESTAMP,
    to_date TIMESTAMP,
    icao VARCHAR(10),
    response TEXT,
    PRIMARY KEY (from_date, to_date, icao)
);
