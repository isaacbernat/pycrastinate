from itertools import chain, repeat
from datetime import datetime


def nested_report(config, data, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts"""
    ind = depth*config.get("indent", "  ")
    if isinstance(data, list):
        max_width = config["max_width"]
        col_separator = config["column_separator"]
        col_order = config["column_order"]
        for line in data:
            str_attrs = [str(el) for el in (line[attr] for attr in col_order)]
            yield (ind + col_separator.join(str_attrs))[:max_width]
    else:
        for key, val in data.items():
            yield chain(
                ["{}{}".format(ind, key)],
                chain.from_iterable(
                    repeat(el, 1) if isinstance(el, str)
                    else el for el in nested_report(config, val, depth+1)))


def text_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    config["indent"] = config.get("indent", "  ")
    config["column_separator"] = config.get("column_separator", "  ")
    config["max_width"] = config.get("max_width", 80)
    hr = "="*config["max_width"]
    config["column_order"] = config.get(
        "column_order", ["token", "line_count", "file_path", "code"])
    column_order = " > ".join(config["column_order"])
    if config.get("timestamp", True):
        column_order += "\nGenerated at: {}".format(datetime.now())
    column_names = [hr, column_order, hr]
    report = chain([column_names], nested_report(config, data))
    return chain.from_iterable(repeat(el, 1) if isinstance(el, str)
                               else el for el in report)
