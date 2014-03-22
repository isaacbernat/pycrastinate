def raise_if_present(config, data):
    """if case-sensitive is not set it defaults to False"""
    config = config.get(__name__.split(".")[-1], {})
    case_sensitive = config.pop("case-sensitive", False)
    if not case_sensitive:
        config = {key: [v.lower() if type(v) == str else v for v in val]
                  for key, val in config.items()}

    for line in data:
        for ckey, cval_list in config.items():
            if ckey in line:
                line_val = line[ckey] if case_sensitive else line[ckey].lower()
                if line_val in cval_list:
                    raise Exception("found '{val}' in '{key}'"
                                    .format(val=line_val, key=ckey))
        yield line
