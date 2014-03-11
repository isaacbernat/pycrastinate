def nested_print(d, config, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts"""
    ind = depth*config["indent"]
    if isinstance(d, list):
        max_width = config["max_width"]
        col_separator = config["column_separator"]
        for l in d:
            str_attrs = [str(a) for a in [l["token"], l["date"], l["email"],
                         l["line_count"], l["file_path"], l["code"]]]
            print((ind + col_separator.join(str_attrs))[:max_width])
    else:
        for k, v in d.items():
            print("{}{}".format(ind, k))
            nested_print(v, config, depth+1)


def print_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    config["indent"] = config.get("indent", "  ")
    config["column_separator"] = config.get("column_separator", "  ")
    config["max_width"] = config.get("max_width", 80)
    print("="*config["max_width"])
    print("token > date > author > line > source")
    print("="*config["max_width"])
    nested_print(data, config)
