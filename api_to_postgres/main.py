import logging
from datetime import datetime

from dotenv import load_dotenv
from Io import closeDB, connectDB, write_checkpoint
from utils import fetch_airport_data, split_into_12_hour_segments_with_checkpoint

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

START_DATE = datetime(2024, 9, 1)
END_DATE = datetime(2024, 9, 20)

if __name__ == "__main__":
    try:
        conn = connectDB()
        cursor = conn.cursor()

        date_segemnts = split_into_12_hour_segments_with_checkpoint(
            START_DATE, END_DATE
        )

        for from_date, to_date in date_segemnts:
            data = fetch_airport_data(from_date, to_date, "EFHK")
            cursor.execute(
                """
                INSERT INTO airport.raw (from_date, to_date, icao, response)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    data["from_date"],
                    data["to_date"],
                    data["icao"],
                    data["response"],
                ),
            )
            conn.commit()
            write_checkpoint(from_date, to_date)
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {e}")
        raise
    finally:
        cursor.close()
        closeDB(conn)
