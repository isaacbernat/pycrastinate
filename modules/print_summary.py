def nested_print(d, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts"""
    if isinstance(d, list):
        for l in d:
            print("{}  {}  {}  {}  {}  {}".format(l["token"], l["date"], l["email"], l["line_count"], l["file_path"], l["code"])[:80])
    else:
        for k, v in d.items():
            print("         -------- {} --------".format(k))
            nested_print(v, depth+1)


def print_summary(config, data):
    print "token |   date    |     author     |line|  source"
    print "====================================================="
    nested_print(data)
