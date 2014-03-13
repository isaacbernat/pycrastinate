#!/usr/bin/env python
import config
from collections import OrderedDict
from functools import reduce


def run(pipeline=config.pipeline, config=config.data, enclose=config.enclose):
    return reduce(lambda results, func: enclose(func, (config, results)),
                  OrderedDict(sorted(pipeline.items())).values(), [])

if __name__ == "__main__":
    run()
