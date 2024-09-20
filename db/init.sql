CREATE SCHEMA IF NOT EXISTS airport;

CREATE TABLE IF NOT EXISTS airport.raw (
    from_date TIMESTAMP,
    to_date TIMESTAMP,
    icao VARCHAR(10),
    response TEXT,
    PRIMARY KEY (from_date, to_date, icao)
);
