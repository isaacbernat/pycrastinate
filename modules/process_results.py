from collections import deque


def process_results(config, data):
    config = config.get(__name__.split(".")[-1], {})
    drop = config.get("drop", True)
    if drop:
        deque(data, maxlen=0)
    return list(data)
