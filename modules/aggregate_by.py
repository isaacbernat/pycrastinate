from collections import defaultdict


def aggregate_keys(list_data, keys, config):
    if not keys:
        return list_data

    agg = defaultdict(list)
    for d in list_data:
        val = d[keys[0]] if config["case-sensitive"]\
            else str(d[keys[0]]).upper()
        agg[val].append(d)
    return {k: aggregate_keys(v, keys[1:], config) for k, v in agg.items()}


def aggregate_by(config, data):
    """if case-sensitive is not set it defaults to False"""
    config = config.get(__name__.split(".")[-1], {})
    config["case-sensitive"] = config.get("case-sensitive", False)
    return aggregate_keys(data, config["keys"], config)
