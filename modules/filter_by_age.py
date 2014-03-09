import datetime


def filter_by_age(config, data):
    config = config.get(__name__.split(".")[-1], {})
    today = datetime.date.today()
    old = datetime.timedelta(config.get("oldest", 999999))
    early = datetime.timedelta(config.get("earliest", 0))

    return (t for t in data
            if t["date"] + early < today and t["date"] + old > today)
