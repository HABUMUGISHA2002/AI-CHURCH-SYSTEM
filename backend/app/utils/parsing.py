from datetime import datetime


def parse_iso_datetime(value, field_name):
    if not value:
        raise ValueError(f"{field_name} is required")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO datetime") from exc
