def print_summary(config, data):
    report = "\n".join(data)
    yield report
    print(report)
