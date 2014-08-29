import os
import codecs


def save_to_file(config, data):
    config = config[__name__.split(".")[-1]]
    filename = config.get("filename", "pycrastinate report.txt")
    full_path = os.path.join(config.get("path", "./"), filename)
    if not config.get("overwrite", False) and os.path.exists(full_path):
        raise Exception("'{}' already exists".format(filename))
    with codecs.open(full_path, "w", "utf-8") as f:
        for d in data:
            f.write(d)
            yield d
