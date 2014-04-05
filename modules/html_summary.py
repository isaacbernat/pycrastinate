from itertools import chain, repeat
from datetime import datetime


def nested_report(data, table_bp, columns, depth=2):
    """Assumes that all levels are nested dicts until a list of dicts"""
    if isinstance(data, list):
        yield table_bp
        for line in data:
            tds = ["<td>{}</td>".format(el) for el in
                  [line[col] for col in columns]]
            yield "<tr>{}</tr>".format("".join(tds))
        yield "<tbody></table>"
    else:
        for key, val in data.items():
            yield chain(
                ["<h{}>{}</h{}>".format(depth, key, depth)],
                chain.from_iterable(
                    repeat(el, 1) if isinstance(el, str)
                    else el for el in nested_report(
                        val, table_bp, columns, depth+1)))


def html_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    title = config.get("title", "Pycrastinate HTML report")
    columns = config.get("columns", ["token", "date", "email", "line_count",
                         "file_path", "code"])
    css_rules = "\n".join(config.get("css",
                          ["td{font-family: monospace; border=1}"]))
    css = '<style type="text/css">{}</style>'.format(css_rules)
    html_start = ["<html><head>{}</head><body><h1>{}</h1>".format(css, title)]
    html_end = ["</body></html>"]
    if config.get("timestamp", True):
        html_start.append("<p>Generated at: {}</p>".format(datetime.now()))
    table_bp = "<table><thead><tr>{}</tr></thead><tbody>".format("".join(
        ("<th>{}</th>".format(col) for col in columns)))
    report = chain([html_start],
                   nested_report(data, table_bp, columns),
                   [html_end])
    return chain.from_iterable(repeat(el, 1) if isinstance(el, str)
                               else el for el in report)
