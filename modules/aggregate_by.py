from collections import defaultdict


def aggregate_by(config, data):
    aggregated = defaultdict(list)
    config = config.get(__name__.split(".")[-1], {})
    key = config["keys"][0]

    for d in data:
        aggregated[d[key]].append(d)
    return aggregated
