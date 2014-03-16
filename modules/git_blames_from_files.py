import subprocess
import datetime
import re
import codecs


def git_blames_from_files(config, data):
    def prepare_regexes():
        tokens_re = u"|".join(config["tokens"])
        case_sensitive = config.get("case-sensitive", False)
        flags = 0 if case_sensitive else re.IGNORECASE
        return {
            "blame": re.compile(u".*({})".format(tokens_re), flags),
            "date": re.compile(u"(\d{4})-(\d{2})-(\d{2})"),
            "email": re.compile(u"<(.*@.*)>"),
            "token": re.compile(u"({})".format(tokens_re), flags),
        }

    def process_blame_line(process_line=True):
        if process_line:
            blame = subprocess.Popen("git blame -e {}".format(code_file),
                                     stdout=subprocess.PIPE, shell=True)
            blame = blame.stdout.read()
            if not blame:
                return
            blame = blame.decode("utf-8").split("\n")[count]
            email = re.search(regex["email"], blame)
            email = email.group(1) if email else ""
            date = re.search(regex["date"], blame).groups()
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            code = u"".join(blame.split(")")[1:]).strip()
            return {
                #[2:] because we skip the initial "./"
                "file_path": code_file[2:],
                "code": code,
                "date": date,
                "email": email,
                "line_count": count+1,
                "token": re.search(regex["token"], code).group(), }

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    for code_file in data:
        with codecs.open(code_file, 'rb', "utf-8") as cf:
            for count, content in enumerate(cf):
                line = process_blame_line(re.match(regex["blame"], content))
                if line:
                    yield line
