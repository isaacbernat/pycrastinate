from collections import defaultdict


def aggregate_by(config, data):
    """if case-sensitive is not set it defaults to False"""
    config = config.get(__name__.split(".")[-1], {})
    case_sensitive = config.pop("case-sensitive", False)
    key = config["keys"][0]
    aggregated = defaultdict(list)
    for d in data:
        val = d[key] if case_sensitive else str(d[key]).upper()
        aggregated[val].append(d)
    return aggregated
