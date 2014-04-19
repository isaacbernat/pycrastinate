def exclude(config, data):
    def filter_line(line):
        for key, test_list in config.items():
            for t in test_list:
                for val in t["values"]:
                    for func in t["functions"]:
                        if func(line.get(key), val):
                            return
        return line

    config = config.get(__name__.split(".")[-1], {})
    return (d for d in (filter_line(d) for d in data) if d)
