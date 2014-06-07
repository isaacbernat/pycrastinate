#!/usr/bin/env python
import sys
from collections import OrderedDict
from functools import reduce


def run(pipeline, config, enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])

if __name__ == "__main__":
    config = "config" if len(sys.argv) == 1 else sys.argv[1].split(".")[0]
    exec("import {}".format(config))
    run(config.pipeline, config.data, config.enclose)
