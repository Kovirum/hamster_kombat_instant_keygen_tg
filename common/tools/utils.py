from datetime import datetime, timezone


def get_timestamp() -> str:
    date = datetime.now(timezone.utc)
    formatted_time = date.strftime("%d.%m %H:%M:%S UTC")
    return formatted_time


def get_date() -> str:
    date = datetime.now(timezone.utc)
    formatted_date = date.strftime("%d.%m.%Y UTC")
    return formatted_date
