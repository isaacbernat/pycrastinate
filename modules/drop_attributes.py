def drop_attributes(config, data):
    config = config.get(__name__.split(".")[-1], {})
    for attr in config.get("attr_list", []):
        for d in data:
            d.pop(attr, None)
    return (d for d in data if d)
