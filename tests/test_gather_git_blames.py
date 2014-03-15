import nose.tools as nt
from pycrastinate import run
from modules.gather_git_blames_shell import gather_git_blames_shell
from modules.gather_git_blames_python import gather_git_blames_python


class TestGatherGitBlames(object):
    def setup(self):
        self.config = {self.module: {
            "init_path": "./tests/aux_files",
            "tokens": {
                "todo": 0,
                "fixme": 1,
            },
            "file_sufixes": [".py", ".rb"],
            "default_email": "tech@wrapp.com",
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
            return [d["file_path"][-3:] for d in data]

        sufixes = filter_sufixes()
        self.config[self.module]["file_sufixes"] = [".py"]
        sufixes_py = filter_sufixes()
        sub_sufixes_python = [s for s in sufixes if s[-3:] == ".py"]

        nt.assert_true(len(sufixes) > len(sub_sufixes_python))
        nt.assert_equals(len(sufixes_py), len(sub_sufixes_python))
        for sp in sufixes_py:
            nt.assert_equals(sp, ".py")

    def filtered_tokens(self):
        def filter_tokens():
            data = run(self.pipeline, self.config)
            return [d["token"].lower() for d in data]

        tokens = filter_tokens()
        self.config[self.module]["tokens"] = {"todo": 0}
        tokens_todo = filter_tokens()
        sub_tokens_todo = [t for t in tokens if t == "todo"]

        nt.assert_true(len(tokens) > len(sub_tokens_todo))
        nt.assert_equals(len(tokens_todo), len(sub_tokens_todo))
        for td in tokens_todo:
            nt.assert_equals(td, "todo")


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


class TestGatherGitBlamesPython(TestGatherGitBlames):
    pipeline = {100: gather_git_blames_python}
    module = gather_git_blames_python.__name__

    def test_gathered_fields(self):
        fields = ["code", "date", "email", "file_path", "line_count", "token"]
        self.gathered_fields(fields)

    def test_filtered_sufixes(self):
        self.filtered_sufixes()

    def test_filtered_tokens(self):
        self.filtered_tokens()
