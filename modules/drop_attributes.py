def drop_attributes(config, data):
    config = config.get(__name__.split(".")[-1], {})
    for d in data:
        perm_d = d
        for attr in config.get("attr_list", []):
            perm_d.pop(attr, None)
        if perm_d:
            yield perm_d
