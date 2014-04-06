import subprocess
import datetime
import re
import codecs
import os


def git_blames_from_files(config, data):
    def prepare_regexes():
        tokens_re = u"|".join(config["tokens"])
        case_sensitive = config.get("case-sensitive", False)
        flags = 0 if case_sensitive else re.IGNORECASE
        return {
            "blame": re.compile(u".*({})".format(tokens_re), flags),
            "date": re.compile(u"(\d{4})-(\d{2})-(\d{2})"),
            "email": re.compile(u"<([^ ]+@[^ ]+)>"),
            "token": re.compile(u"({})".format(tokens_re), flags),
        }

    def process_blame_line():
        filename = code_file.split("/")[-1]
        pathname = code_file.split(filename)[0]
        os.chdir(pathname)
        lines_text = "".join(" -L {n},{n}".format(n=nu) for nu in line_numbers)
        blames = subprocess.Popen("git blame -e {} {}".format(
            filename, lines_text), stdout=subprocess.PIPE,
            shell=True).stdout.read().decode("utf-8").split("\n")
        os.chdir(init_dir)
        for blame, line in zip(blames, line_numbers):
            email = re.search(regex["email"], blame)
            email = email.group(1) if email else ""
            date = datetime.date(
                *[int(d) for d in re.search(regex["date"], blame).groups()])
            code = u"".join(blame.split(")")[1:]).strip()
            yield {
                "file_path": code_file,
                "code": code,
                "date": date,
                "email": email,
                "line_count": line,
                "token": re.search(regex["token"], code).group(), }

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    init_dir = os.getcwd()
    for code_file in data:
        with codecs.open(code_file, 'rb', "utf-8") as cf:
            line_numbers = []
            for count, content in enumerate(cf, start=1):
                if re.match(regex["blame"], content):
                    line_numbers.append(count)
            if line_numbers:
                for line in process_blame_line():
                    yield line
