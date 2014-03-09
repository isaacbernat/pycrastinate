from collections import defaultdict


def aggregate_by_email(config, data):
    aggregated = defaultdict(list)
    for t in data:
        aggregated[t["email"]].append(t)
    return aggregated
