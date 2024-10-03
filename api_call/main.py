import csv
import json
import os
import sys
from datetime import datetime, timedelta
from io import StringIO

# Add the package directory to the Python path
package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "package"))
sys.path.append(package_dir)

import boto3
import requests


def generate_date_ranges_list(start_date: datetime, end_date: datetime) -> list:
    date_ranges = []
    current_date = start_date
    interval = timedelta(hours=12)

    while current_date < end_date:
        group = []
        for _ in range(4):
            range_end = min(current_date + interval, end_date)
            group.append((current_date, range_end))
            current_date = range_end
            if current_date >= end_date:
                break
        if group:
            date_ranges.append(group)

    return date_ranges


def fetch_and_write_flight_data(event, context):
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    API_KEY = os.environ.get("API_KEY")
    START_DATE = os.environ.get("START_DATE")
    END_DATE = os.environ.get("END_DATE")
    AIRPORT_ICAO = os.environ.get("AIRPORT_ICAO")
    s3 = boto3.client("s3")

    # Validate and parse START_DATE and END_DATE
    try:
        start_date = datetime.fromisoformat(START_DATE)
        end_date = datetime.fromisoformat(END_DATE)
    except ValueError:
        raise ValueError(
            "START_DATE and END_DATE must be in ISO format (YYYY-MM-DDTHH:MM)"
        )

    for date_range in generate_date_ranges_list(start_date, end_date):
        # Create a new StringIO object for each date range
        csv_buffer = StringIO()
        fieldnames = [
            "airport_icao",
            "timestamp",
            "fromdate",
            "todate",
            "response_code",
            "response",
        ]
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        # Generate file key based on start and end dates and AIRPORT_ICAO
        file_key = f"{AIRPORT_ICAO}/{date_range[0][0].strftime('%Y%m%d_%H%M')}_to_{date_range[-1][-1].strftime('%Y%m%d_%H%M')}.csv"

        for from_date, to_date in date_range:
            url = f"https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/airports/Icao/{AIRPORT_ICAO}/{from_date.isoformat()}/{(to_date.isoformat())}"
            headers = {
                "accept": "application/json",
                "x-magicapi-key": API_KEY,
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

            csv_data = {
                "airport_icao": AIRPORT_ICAO,
                "fromdate": from_date.isoformat(),
                "todate": to_date.isoformat(),
                "timestamp": datetime.now().isoformat(),
                "response_code": str(response.status_code),
                "response": json.dumps(response.json()),
            }

            writer.writerow(csv_data)

        # Upload the CSV data to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=csv_buffer.getvalue().encode("utf-8"),
            ACL="bucket-owner-full-control",
        )
        print(f"Successfully uploaded '{file_key}' to bucket '{BUCKET_NAME}'.")
