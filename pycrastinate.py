#!/usr/bin/env python
import sys
from collections import OrderedDict
from functools import reduce


def run(pipeline, config, enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])

if __name__ == "__main__":
    _cfg_name = "config" if len(sys.argv) == 1 else sys.argv[1].split(".")[0]
    exec("import {}".format(_cfg_name))
    _cfg = eval(_cfg_name)
    run(_cfg.pipeline, _cfg.data, _cfg.enclose)
