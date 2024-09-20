import logging
import os
from datetime import datetime, timedelta

import requests
from Io import read_checkpoint


def fetch_airport_data(from_date: datetime, to_date: datetime, icao: str) -> dict:
    try:
        if (to_date - from_date) > timedelta(hours=12):
            raise ValueError(
                f"The time range between from_date: {from_date} and to_date: {to_date} must be 12 hours or less."
            )

        url = f"https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/airports/Icao/{icao}/{from_date.isoformat()}/{(to_date.isoformat())}"
        headers = {
            "accept": "application/json",
            "x-magicapi-key": os.getenv("API_KEY"),
        }
        params = {
            "direction": "Both",
            "withLeg": "false",
            "withCancelled": "true",
            "withCodeshared": "true",
            "withCargo": "true",
            "withPrivate": "true",
            "withLocation": "false",
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {
            "from_date": from_date,
            "to_date": to_date,
            "icao": icao,
            "response": response.text,
        }
    except ValueError as e:
        logging.error(f"Value error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTPs error: {e}")
        raise
    except Exception as e:
        logging.error(f"Error fetching airport data: {e}")
        raise


def split_into_12_hour_segments_with_checkpoint(
    start_date: datetime, end_date: datetime
) -> list:
    if start_date >= end_date:
        raise ValueError("start_date must be earlier than end_date")

    (checkpoint_start, _) = read_checkpoint()
    segments = []
    current_start = start_date

    while current_start < end_date:
        current_end = min(current_start + timedelta(hours=12), end_date)
        if checkpoint_start == None or current_start > checkpoint_start:
            segments.append((current_start, current_end))
        current_start = current_end

    return segments
