import logging
import os
from datetime import datetime

import psycopg2


def write_checkpoint(dt, filename="checkpointing.txt"):
    with open(filename, "w") as f:
        f.write(dt.isoformat())


def read_checkpoint(filename="checkpointing.txt"):
    with open(filename, "r") as f:
        dt_str = f.read()
        return datetime.fromisoformat(dt_str)


def connectDB():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        logging.info("Connected to database successfully")
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise


def closeDB(conn):
    try:
        conn.close()
        logging.info("Database connection closed successfully")
    except Exception as e:
        logging.error(f"Error closing database connection: {e}")
        raise
