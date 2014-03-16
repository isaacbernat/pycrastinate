import nose.tools as nt
from modules.gather_files import gather_files

module = gather_files.__name__


class TestGatherFiles(object):
    def setup(self):
        self.config = {module: {
            "root_paths": ["./tests/aux_files"],
            "file_sufixes": [".py", ".rb"],
            }
        }

    def test_filtered_sufixes(self):
        sufixes = list(gather_files(self.config, []))
        sub_sufixes_python = [s for s in sufixes if s[-3:] == ".py"]
        self.config[module]["file_sufixes"] = [".py"]
        sufixes_py = list(gather_files(self.config, []))
        nt.assert_true(len(sufixes) > len(sub_sufixes_python))
        nt.assert_true(len(sufixes_py) > 0)
        nt.assert_equals(sorted(sufixes_py), sorted(sub_sufixes_python))

    def test_files_from_multiple_root_paths(self):
        self.config[module]["root_paths"] = ["./enclose"]
        files_enclose = list(gather_files(self.config, []))
        self.config[module]["root_paths"] =\
            ["./tests/aux_files", "./enclose"]
        files = list(gather_files(self.config, []))
        sub_files_enclose = [f for f in files if f.startswith("./enclose")]
        nt.assert_true(len(files) > len(sub_files_enclose))
        nt.assert_true(len(files_enclose) > 0)
        nt.assert_equals(sorted((files_enclose)), sorted(sub_files_enclose))
