import nose.tools as nt
from modules.git_blames_from_files import git_blames_from_files

module = "git_blames_from_files"
data = ['./tests/aux_files/test_python.py',
        './tests/aux_files/test_ruby.rb']


class TestGitBlamesFromFiles(object):
    def setup(self):
        self.config = {module: {
            "tokens": ["TODO", "FIXME"],
            "case-sensitive": False,
            "include_committer": False,
            }
        }

    def test_gathered_fields(self):
        fields = ["code", "date", "email", "file_path", "line_count",
                  "token"]
        blame_data = list(git_blames_from_files(self.config, data))
        nt.assert_true(len(blame_data) > 0)
        for line in blame_data:
            nt.assert_equal(sorted(fields), sorted(line.keys()))

    def test_filtered_tokens(self):
        def filter_tokens():
            blame_data = git_blames_from_files(self.config, data)
            return [d["token"].lower() for d in blame_data]

        tokens = filter_tokens()
        self.config[module]["tokens"] = {"todo": 0}
        tokens_todo = filter_tokens()
        sub_tokens_todo = [t for t in tokens if t == "todo"]

        nt.assert_true(len(tokens) > len(sub_tokens_todo))
        nt.assert_true(len(tokens_todo) > 0)
        nt.assert_equals(sorted(tokens_todo), sorted(sub_tokens_todo))

    def test_case_sensitivity(self):
        def get_tokens():
            blame_data = git_blames_from_files(self.config, data)
            return [d["token"] for d in blame_data]

        tokens = get_tokens()
        self.config[module]["case-sensitive"] = True
        tokens_upper = get_tokens()
        sub_tokens_upper = [t for t in tokens if t.upper() == t]

        nt.assert_true(len(tokens) > len(sub_tokens_upper))
        nt.assert_true(len(tokens_upper) > 0)
        nt.assert_equals(sorted(tokens_upper), sorted(sub_tokens_upper))
