import subprocess
import os
import datetime
import re
import codecs


def gather_git_blames_python(config, *args):
    def prepare_regexes():
        tokens_re = u"|".join(config["tokens"].keys())
        sufix_re = u"|".join(config["file_sufixes"])
        case_sensitive = config.get("case-sensitive", False)
        flags = 0 if case_sensitive else re.IGNORECASE
        return {
            "blame": re.compile(u".*({})".format(tokens_re), flags),
            "date": re.compile(u"(\d{4})-(\d{2})-(\d{2})"),
            "email": re.compile(u"<(.*@.*)>"),
            "token": re.compile(u"({})".format(tokens_re), flags),
            "sufix": re.compile(u".*({})$".format(sufix_re), re.IGNORECASE),
        }

    def list_files(path="."):
        return (os.path.join(root, f) for root, dirs, files in os.walk(path)
                for f in files if re.match(regex["sufix"], f))

    def process_blame_line(will_be_processed=True):
        if will_be_processed:
            blame = subprocess.Popen("git blame -e {}".format(code_file),
                                     stdout=subprocess.PIPE, shell=True)
            blame = blame.stdout.read()
            if not blame:
                return
            blame = blame.decode("utf-8").split("\n")[count]
            email = re.search(regex["email"], blame)
            email = email.group(1) if email else config["default_email"] or u""
            date = re.search(regex["date"], blame).groups()
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            code = u"".join(blame.split(")")[1:]).strip()
            return {
                "code": code,
                "date": date,
                "email": email,
                #we skip the initial "./"
                "file_path": code_file[2:],
                "line_count": count+1,
                "token": re.search(regex["token"], code).group(), }

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    for code_file in list_files(config["init_path"]):
        with codecs.open(code_file, 'rb', "utf-8") as cf:
            for count, content in enumerate(cf):
                do = process_blame_line(re.match(regex["blame"], content))
                if do:
                    yield do
