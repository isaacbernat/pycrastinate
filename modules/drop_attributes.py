def drop_attributes(config, data):
    def filter_attr(line):
        return {k: v for k, v in line.items() if k not in attr_list}

    attr_list = config.get(__name__.split(".")[-1], {}).get("attr_list", [])
    return (d for d in (filter_attr(line) for line in data) if d)
