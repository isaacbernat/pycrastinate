import subprocess
import datetime
import re
import os
from modules import extract_from_files as ex


def prepare_regexes(config):
    tokens_re = u"|".join(config["tokens"])
    case_sensitive = config.get("case-sensitive", False)
    flags = 0 if case_sensitive else re.IGNORECASE
    return {
        "hit": re.compile(u".*({})".format(tokens_re), flags),
        "date": re.compile(u"(\d{4})-(\d{2})-(\d{2})"),
        "email": re.compile(u"<([^ ]+@[^ ]+)>"),
        "token": re.compile(u"({})".format(tokens_re), flags),
    }


def process_blame_lines(pi):
    code_file = pi["code_file"]
    line_numbers = pi["line_info"].keys()
    regex = pi["regex"]
    init_dir = pi["init_dir"]
    filename = code_file.split("/")[-1]
    pathname = code_file.split(filename)[0]
    os.chdir(pathname)
    lines_text = ["-L {n},{n}".format(n=nu) for nu in line_numbers]
    blames = [subprocess.Popen("git blame -e {} {}".format(
        filename, line_text), stdout=subprocess.PIPE,
        shell=True).stdout.read().decode("utf-8") for line_text in lines_text]
    os.chdir(init_dir)
    for blame, line in zip(blames, line_numbers):
        email = re.search(regex["email"], blame)
        email = email.group(1) if email else ""
        try:
            date = datetime.date(
                *[int(d) for d in re.search(regex["date"], blame).groups()])
        except AttributeError:
            # not committed, so no commit date and we skip it
            continue
        code = u"".join(blame.split(")")[1:]).strip()
        yield {
            "file_path": code_file,
            "code": code,
            "date": date,
            "email": email,
            "line_count": line,
            "token": re.search(regex["token"], code).group(), }

ex.mod_name = __name__
ex.prepare_regexes = prepare_regexes
ex.process_lines = process_blame_lines
git_blames_from_files = ex.extract_from_files
