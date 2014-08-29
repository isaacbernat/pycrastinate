import re
from modules import extract_from_files as ex


def prepare_regexes(config):
    tokens_re = u"|".join(config["tokens"])
    flags = 0 if config.get("case-sensitive", False) else re.IGNORECASE
    return {"hit": re.compile(u".*({})".format(tokens_re), flags),
            "token": re.compile(u"({})".format(tokens_re), flags), }


def process_lines(pi):
    code_file = pi["code_file"]
    regex_token = pi["regex"]["token"]
    for line_num, code in pi["line_info"].items():
        yield {"file_path": code_file,
               "code": code,
               "line_count": line_num,
               "token": re.search(regex_token, code).group(), }


ex.mod_name = __name__
ex.prepare_regexes = prepare_regexes
ex.process_lines = process_lines
regex_from_files = ex.extract_from_files
