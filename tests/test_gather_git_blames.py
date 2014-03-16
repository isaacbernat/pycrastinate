import nose.tools as nt
from pycrastinate import run
from modules.gather_git_blames_shell import gather_git_blames_shell


class TestGatherGitBlames(object):
    def setup(self):
        self.config = {self.module: {
            "init_path": "./tests/aux_files",
            "tokens": ["TODO", "FIXME"],
            "file_sufixes": [".py", ".rb"],
            }
        }

    def gathered_fields(self, fields):
        data = list(run(self.pipeline, self.config))
        nt.assert_true(len(data) > 0)
        for d in data:
            nt.assert_equal(sorted(fields), sorted(d.keys()))

    def filtered_sufixes(self):
        def filter_sufixes():
            data = run(self.pipeline, self.config)
            return [d["file_path"] for d in data]

        sufixes = filter_sufixes()
        self.config[self.module]["file_sufixes"] = [".py"]
        sufixes_py = filter_sufixes()
        sub_sufixes_python = [s for s in sufixes if s[-3:] == ".py"]

        nt.assert_true(len(sufixes) > len(sub_sufixes_python))
        nt.assert_true(len(sufixes_py) > 0)
        nt.assert_equals(sorted(sufixes_py), sorted(sub_sufixes_python))

    def filtered_tokens(self):
        def filter_tokens():
            data = run(self.pipeline, self.config)
            return [d["token"].lower() for d in data]

        tokens = filter_tokens()
        self.config[self.module]["tokens"] = {"todo": 0}
        tokens_todo = filter_tokens()
        sub_tokens_todo = [t for t in tokens if t == "todo"]

        nt.assert_true(len(tokens) > len(sub_tokens_todo))
        nt.assert_true(len(tokens_todo) > 0)
        nt.assert_equals(sorted(tokens_todo), sorted(sub_tokens_todo))

    def case_sensitivity(self):
        def get_tokens():
            data = run(self.pipeline, self.config)
            return [d["token"] for d in data]

        tokens = get_tokens()
        self.config[self.module]["case-sensitive"] = True
        tokens_upper = get_tokens()
        sub_tokens_upper = [t for t in tokens if t.upper() == t]

        nt.assert_true(len(tokens) > len(sub_tokens_upper))
        nt.assert_true(len(tokens_upper) > 0)
        nt.assert_equals(sorted(tokens_upper), sorted(sub_tokens_upper))


class TestGatherGitBlamesShell(TestGatherGitBlames):
    pipeline = {100: gather_git_blames_shell}
    module = gather_git_blames_shell.__name__

    def test_gathered_fields(self):
        fields = ["commit_hash", "code", "date", "email", "file_path",
                  "line_count", "token", "summary", "author", "author-tz"]
        self.gathered_fields(fields)

    def test_filtered_sufixes(self):
        self.filtered_sufixes()

    def test_filtered_tokens(self):
        self.filtered_tokens()

    def test_case_sensitivity(self):
        self.case_sensitivity()
