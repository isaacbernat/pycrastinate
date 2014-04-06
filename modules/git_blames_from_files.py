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
        blame = subprocess.Popen("git blame -e {} -L {},{}".format(
            filename, count, count), stdout=subprocess.PIPE,
            shell=True).stdout.read().decode("utf-8")
        os.chdir(init_dir)
        email = re.search(regex["email"], blame)
        email = email.group(1) if email else ""
        date = re.search(regex["date"], blame).groups()
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        code = u"".join(blame.split(")")[1:]).strip()
        return {
            "file_path": code_file,
            "code": code,
            "date": date,
            "email": email,
            "line_count": count,
            "token": re.search(regex["token"], code).group(), }

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    init_dir = os.getcwd()
    for code_file in data:
        with codecs.open(code_file, 'rb', "utf-8") as cf:
            for count, content in enumerate(cf, start=1):
                if re.match(regex["blame"], content):
                    yield process_blame_line()
