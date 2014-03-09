def raise_if_present(config, data):
    """if case-sensitive is not set it defaults to False"""
    config = config.get(__name__.split(".")[-1], {})
    case_sensitive = config.pop("case-sensitive", False)
    if not case_sensitive:
        config_str = {key: [v.lower() for v in val if type(v) == str]
                      for key, val in config.items()}

        config = {k: v for k, v in config.items() if k not in config_str}
        config.update(config_str)
    for line in data:
        for ckey, cval_list in config.items():
            if ckey in line:
                line_val = line[ckey] if case_sensitive else line[ckey].lower()
                if line_val in cval_list:
                    raise Exception("found '{val}' in '{key}'"
                                    .format(val=line_val, key=ckey))
        yield line
