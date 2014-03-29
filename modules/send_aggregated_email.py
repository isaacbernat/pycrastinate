import re
from modules.send_email import *
from modules.process_results import process_results


def nested_report(config, data, depth=0):
    """Assumes that all levels are nested dicts until a list of dicts.
    Asumes e-mails to send are the keys of some of these nodes
    Assumes input is not mutable"""
    if isinstance(data, list):
        return
    else:
        for key, val in data.items():
            if re.match(config["email_re"], key):
                body = config["render_function"](config, val)
                config["to"] = config.get("to", []) + [key.lower()]
                process_results({}, send_email({"send_email": config}, body))
            else:
                nested_report(config, val, depth+1)


def send_aggregated_email(config, data):
    config = config.get(__name__.split(".")[-1], {})
    config["email_re"] = re.compile(u"[^ ]+@[^ ].[^ ]", re.IGNORECASE)
    config["smtp"] = prepare_smtp(config)
    nested_report(config, data)
    quit_smtp(config["smtp"])
    return data
