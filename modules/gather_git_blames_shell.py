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
        sed = 'sed s"/\/\///"'
        xargs = 'xargs -P4 -n6 git'
        cat = 'cat'
        one_liner = " | ".join([grep, cut, awk, sed, xargs, cat])

        return subprocess.Popen(one_liner, stdout=subprocess.PIPE, shell=True)\
            .stdout.read().decode().split("\n")

    def process_blame_output(blames_lines):
        normalised_lines = list(normalise(blame_lines))
        #TODO try to use a generator instead of iterating over xrange list
        for commit_line in range(0, len(normalised_lines)-1, 12):
            commit_hash = normalised_lines[commit_line]
            line_count = re.match(regex["line_count_re"],
                                  normalised_lines[commit_line]).group(1)
            email = normalised_lines[commit_line+2][len("author-mail <"):-1]
            date = datetime.date.fromtimestamp(
                int(normalised_lines[commit_line+3][len("author-time "):]))
            summary = normalised_lines[commit_line+9][len("summary "):]
            file_path = normalised_lines[commit_line+10][len("filename "):]
            code = normalised_lines[commit_line+11].strip()
            token = re.search(regex["tokens_compiled"], code).group()

            yield {
                "commit_hash": commit_hash,
                "code": code,
                "date": date,
                "email": email,
                "file_path": file_path,
                "line_count": line_count,
                "token": token,
                "summary": summary,
            }

    config = config[__name__.split(".")[-1]]
    regex = prepare_regexes()
    blame_lines = get_blames_lines()
    return process_blame_output(blame_lines)
