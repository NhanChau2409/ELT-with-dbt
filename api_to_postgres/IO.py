import logging
import os
from datetime import datetime

import psycopg2


def write_checkpoint(
    from_date: datetime, to_date: datetime, filename="checkpointing.txt"
):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(filename, "w") as f:
        f.write(from_date.isoformat())
        f.write("\n")
        f.write(to_date.isoformat())


def read_checkpoint(filename="checkpointing.txt"):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open(filename, "r") as f:
        from_date_str = f.readline().strip()
        to_date_str = f.readline().strip()

        if not from_date_str or not to_date_str:
            return (None, None)

        from_date = datetime.fromisoformat(from_date_str)
        to_date = datetime.fromisoformat(to_date_str)

        return (from_date, to_date)


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
