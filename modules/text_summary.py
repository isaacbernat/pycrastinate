from itertools import chain, repeat


def nested_report(d, config, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts"""
    ind = depth*config["indent"]
    if isinstance(d, list):
        max_width = config["max_width"]
        col_separator = config["column_separator"]
        for l in d:
            str_attrs = [str(a) for a in [l["token"], l["date"], l["email"],
                         l["line_count"], l["file_path"], l["code"]]]
            yield (ind + col_separator.join(str_attrs))[:max_width]
    else:
        for k, v in d.items():
            yield chain(
                ["{}{}".format(ind, k)],
                chain.from_iterable(
                    repeat(l, 1) if isinstance(l, str)
                    else l for l in nested_report(v, config, depth+1)))


def text_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    config["indent"] = config.get("indent", "  ")
    config["column_separator"] = config.get("column_separator", "  ")
    config["max_width"] = config.get("max_width", 80)
    hr = "="*config["max_width"]
    column_order = "token > date > author > line > source"
    column_names = "\n".join([hr, column_order, hr])
    yield column_names
    for iter_lines in nested_report(data, config):
        for line in iter_lines:
            yield line
