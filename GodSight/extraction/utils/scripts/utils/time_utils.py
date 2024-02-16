import pytz
from datetime import datetime

def convert_to_gmt_timestamp(date_str):
    # Define the GMT timezone
    gmt = pytz.timezone('GMT')

    # Parse the date string
    dt_naive = datetime.strptime(date_str, "%Y-%m-%d")

    # Localize the date to GMT
    dt_gmt = gmt.localize(dt_naive)

    # Convert to Unix timestamp
    timestamp = int(dt_gmt.timestamp())

    return timestamp


def get_today_start_gmt_timestamp():
    # Define the GMT timezone
    gmt = pytz.timezone('GMT')

    # Get the current time in GMT
    now_gmt = datetime.now(gmt)

    # Set the time to the start of the day (midnight)
    start_of_today_gmt = now_gmt.replace(hour=0, minute=0, second=0, microsecond=0)

    # Convert to Unix timestamp
    timestamp = int(start_of_today_gmt.timestamp())

    return timestamp
