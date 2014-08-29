from itertools import chain, repeat
from datetime import datetime


def nested_report(config, data, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts"""
    ind = depth * config.get("indent", "  ")
    if isinstance(data, list):
        max_width = config.get("max_width", 80)
        col_separator = config.get("column_separator", "  ")
        col_order = config["columns"]
        for line in data:
            str_attrs = [str(el) for el in (line[attr] for attr in col_order)]
            yield (ind + col_separator.join(str_attrs))[:max_width]
    else:
        for key, val in data.items():
            yield chain(
                ["{}{}".format(ind, key)],
                chain.from_iterable(
                    repeat(el, 1) if isinstance(el, str)
                    else el for el in nested_report(config, val, depth + 1)))


def text_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    config["columns"] = config.get(
        "columns", ["token", "line_count", "file_path", "code"])
    column_order = " > ".join(config["columns"])
    if config.get("timestamp", True):
        column_order += "\nGenerated at: {}".format(datetime.now())
    hr = "=" * config["max_width"]
    report = chain([hr, column_order, hr], nested_report(config, data))
    return chain.from_iterable(repeat(el, 1) if isinstance(el, str)
                               else el for el in report)
