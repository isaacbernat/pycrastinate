#!/usr/bin/env python
import sys
import os
from collections import OrderedDict
from functools import reduce


def run(pipeline, config, enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])

def pycrastinate(full_path):
    sys.path.append(os.path.dirname(os.path.expanduser(full_path)))
    _cfg_name = full_path.split("/")[-1].split(".")[0]
    exec("import {}".format(_cfg_name))
    _cfg = eval(_cfg_name)
    run(_cfg.pipeline, _cfg.data, _cfg.enclose)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        pycrastinate(sys.argv[1])
    else:
        print("You must run pycrastinate with one config file as an argument")
