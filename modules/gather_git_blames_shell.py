import subprocess
import datetime
import re


def gather_git_blames_shell(config, *args):
    def normalise(blame_lines):
        #Sometimes commits have a "previous" line between summary and filename.
        #Sometimes they have not -- porcelain format seems to be inconsistent.
        return (line for line in blame_lines
                if not re.match(regex["previous_or_boundary_re"], line))

    def prepare_regexes():
        raw_tokens_re = u"|".join(config["tokens"].keys())
        tokens_compiled = re.compile(u"({})".format(
            raw_tokens_re), re.IGNORECASE)
        line_count_re = re.compile("[0-9a-f]{40} \d+ (\d+)")
        previous_re = re.compile("(previous [0-9a-f]{40})|boundary")

        return {
            "raw_tokens_re": raw_tokens_re,
            "tokens_compiled": tokens_compiled,
            "line_count_re": line_count_re,
            "previous_or_boundary_re": previous_re,
            }

    def get_blames_lines():
        include_sufixes = u'" --include "*{}"'.format(u'" --include "*'.join(
            config["file_sufixes"])) if config["file_sufixes"] else '"'
        grep = 'grep -E -n -i "{}{} -R {}'.format(
            regex["raw_tokens_re"], include_sufixes, config["init_path"])
        cut = 'cut -d: -f1,2'
        awk = " ".join([
            "awk '{",
            'FS= ":";',
            'split($1, path, "/");',
            'paths="";',
            'fn=path[length(path)];',
            'for(i=0; i<length(path)-1; i++)(paths=paths "/" path[i]);',
            'print "-C " paths "/ blame --line-porcelain -L" $2"," $2 " " fn',
            "}'"])
        sed = 'sed s"/\/\///; s/\:.*//"'
        xargs = 'xargs -P4 -n6 git'
        cat = 'cat'
        one_liner = " | ".join([grep, cut, awk, sed, xargs, cat])

        return subprocess.Popen(one_liner, stdout=subprocess.PIPE, shell=True)\
            .stdout.read().decode("utf-8").split("\n")

    def process_blame_output(blames_lines):
        def initialise_length_dict(include_committer):
            length = {
                "auth": len("author "),
                "mail": len("author-mail <"),
                "date": len("author-time "),
                "tz": len("author-tz "),
                "summ": len("summary "),
                "fn": len("filename "),
            }
            if include_committer:
                length.update({
                    "committer": len("committer "),
                    "committer-mail": len("committer-mail <"),
                    "commit-time": len("committer-time "),
                    "committer-tz": len("author-tz "),
                })
            return length

        def process_commit_lines():
            hash_line = next(commit_lines)
            line_count = re.match(line_count_re, hash_line)
            if not line_count:
                return
            author = next(commit_lines)[length["auth"]:]
            email = next(commit_lines)[length["mail"]:-1]
            int_date = int(next(commit_lines)[length["date"]:])
            date = datetime.date.fromtimestamp(int_date)
            author_tz = next(commit_lines)[length["tz"]:]
            if include_committer:
                committer = next(commit_lines)[length["committer"]:]
                committer_mail =\
                    next(commit_lines)[length["committer-mail"]:-1]
                int_commit_time =\
                    int(next(commit_lines)[length["commit-time"]:])
                committer_date = datetime.date.fromtimestamp(int_commit_time)
                committer_tz = next(commit_lines)[length["committer-tz"]:]
            else:
                for i in range(4):
                    next(commit_lines)
            summary = next(commit_lines)[length["summ"]:]
            file_path = next(commit_lines)[length["fn"]:]
            code = next(commit_lines).strip()
            token = re.search(tokens_compiled, code)
            if token:
                metadata_line = {
                    "author": author,
                    "author-tz": author_tz,
                    "commit_hash": hash_line,
                    "code": code,
                    "date": date,
                    "email": email,
                    "file_path": file_path,
                    "line_count": line_count.group(1),
                    "token": token.group(),
                    "summary": summary,
                }
                if include_committer:
                    metadata_line.update({
                        "commit-author": committer,
                        "commit-emailhash": committer_mail,
                        "commit-date": committer_date,
                        "commit-tz": committer_tz,
                        })
                return metadata_line

        include_committer = config.get("include_committer", False)
        line_count_re = regex["line_count_re"]
        tokens_compiled = regex["tokens_compiled"]
        length = initialise_length_dict(include_committer)
        commit_lines = normalise(blame_lines)
        while commit_lines:
            metadata_line = process_commit_lines()
            if metadata_line:
                yield metadata_line

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    blame_lines = get_blames_lines()
    return process_blame_output(blame_lines)
