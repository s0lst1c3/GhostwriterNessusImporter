from datetime import datetime, timezone


def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)


def get_utc_now_isoformat():
    return get_utc_now().isoformat()
