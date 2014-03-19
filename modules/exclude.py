def exclude(config, data):
    config = config.get(__name__.split(".")[-1], {})
    for d in data:
        skip_d = False
        for k, v in config.items():
            for val in v["values"]:
                skip_d = v["function"](d.get(k), val)
                if skip_d:
                    break
            if skip_d:
                break
        if skip_d:
            continue
        yield d
