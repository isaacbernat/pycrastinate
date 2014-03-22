import os
import re


def gather_files(config, *args):
    def prepare_regexes():
        sufix_re = u"|".join(config["file_sufixes"])
        return {
            "sufix": re.compile(u".*({})$".format(sufix_re), re.IGNORECASE),
        }

    def list_files(path="."):
        return (os.path.join(root, f) for root, dirs, files in os.walk(path)
                for f in files if re.match(regex["sufix"], f))

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    file_list_generators = (list_files(path) for path in config["root_paths"])
    return (f for gen in file_list_generators for f in gen)
