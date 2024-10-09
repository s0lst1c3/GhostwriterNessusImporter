def parse_list(value: str):
    value = value.lstrip("[").rstrip("]")
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_exclude_hosts(settings):
    nessus = settings.get("nessus")
    if not settings or not nessus.get("exclude_hosts"):
        return
    settings.nessus.exclude_hosts = parse_list(nessus.get("exclude_hosts", "[]"))
