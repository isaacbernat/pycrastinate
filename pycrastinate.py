#!/usr/bin/env python
import sys
import os
from collections import OrderedDict
from functools import reduce


def run(pipeline, config, enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        _cfg_path_name = sys.argv[1]
        sys.path.append(os.path.dirname(os.path.expanduser(_cfg_path_name)))
        _cfg_name = _cfg_path_name.split("/")[-1].split(".")[0]
        exec("import {}".format(_cfg_name))
        _cfg = eval(_cfg_name)
        run(_cfg.pipeline, _cfg.data, _cfg.enclose)
    else:
        print("You must run pycrastinate with one config file as an argument")
