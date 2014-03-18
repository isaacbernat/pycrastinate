from itertools import chain, repeat


def nested_report(data, table_bp, depth=2):
    """Assumes that all levels are nested dicts until a list of dicts"""
    if isinstance(data, list):
        yield table_bp
        for line in data:
            tds = ["<td>{}</td>".format(el) for el in
                  [line["token"], line["date"],
                   line["email"], line["line_count"],
                   line["file_path"], line["code"]]]
            yield "<tr>{}</tr>".format("".join(tds))
        yield "<tbody></table>"
    else:
        for key, val in data.items():
            yield chain(
                ["<h{}>{}</h{}>".format(depth, key, depth)],
                chain.from_iterable(
                    repeat(el, 1) if isinstance(el, str)
                    else el for el in nested_report(val, table_bp, depth+1)))


def html_summary(config, data):
    config = config.get(__name__.split(".")[-1], {})
    title = config.get("title", "Pycrastinate HTML report")
    css_rules = "\n".join(config.get("css",
                          ["td{font-family: monospace; border=1}"]))
    css = '<style type="text/css">{}</style>'.format(css_rules)
    yield "<html><head>{}</head><body><h1>{}</h1>".format(css, title)
    table_bp = "<table><thead><tr>{}</tr></thead><tbody>".format("".join(
        ("<th>{}</th>".format(col)
            for col in [
                "token", "date", "author", "line", "source", "comment"])))
    for iter_lines in nested_report(data, table_bp):
        for line in iter_lines:
            yield line
    yield "</body></html>"
