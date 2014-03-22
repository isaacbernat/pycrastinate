import os
import codecs


def save_to_file(config, data):
    config = config[__name__.split(".")[-1]]
    overwrite = config.get("overwrite", False)
    path = config.get("path", "./")
    filename = config.get("filename", "pycrastinate report.txt")
    full_path = os.path.join(path, filename)

    if not overwrite and os.path.exists(full_path):
        raise Exception("'{filename}' already exists in '{path}'"
                        .format(filename=filename, path=path))
    with codecs.open(full_path, "w", "utf-8") as f:
        for d in data:
            f.write(d)
            yield d
