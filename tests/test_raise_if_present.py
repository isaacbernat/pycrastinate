import nose.tools as nt
from modules.raise_if_present import raise_if_present

data = [
    {'code': u'#TODO write cool sotfware', 'token': 'TODO'},
    {'code': u'#FIXME celebrate new year', 'token': 'FIXME'},
    {'code': u'#todo write more tests', 'token': 'todo', 'test': 100},
]

module = raise_if_present.__name__


class TestAssertNotPresent(object):
    def setup(self):
        self.config = {module: {
            "case-sensitive": True,
            "token": ["fixme"],
            },
        }

    def test_returns_unaltered_data(self):
        res = list(raise_if_present(self.config, data))
        nt.assert_equals(res, data)

    def test_case_sensitivity(self):
        list(raise_if_present(self.config, data))
        self.config[module]["case-sensitive"] = False
        try:
            list(raise_if_present(self.config, data))
        except:
            pass
        nt.assert_raises(Exception, "found 'fixme' in 'token'")

    def test_case_insensitive_by_default(self):
        self.config[module].pop("case-sensitive")
        nt.assert_false("case-sensitive" in self.config[module])
        try:
            list(raise_if_present(self.config, data))
        except:
            pass
        nt.assert_raises(Exception, "found 'fixme' in 'token'")

    def test_case_supports_lists_of_elements(self):
        self.config[module]["token"].append("TODO")
        nt.assert_true(len(self.config[module]["token"]) > 1)
        try:
            list(raise_if_present(self.config, data))
        except:
            pass
        nt.assert_raises(Exception, "found 'TODO' in 'token'")

    def test_case_supports_non_string_values(self):
        self.config[module].pop("token")
        self.config[module]["test"] = 100
        nt.assert_true(type(self.config[module]["test"]) != str)
        try:
            list(raise_if_present(self.config, data))
        except:
            pass
        nt.assert_raises(Exception, "found '100' in 'test'")

    def test_case_supports_multiple_keys(self):
        self.config[module]["test"] = 100
        nt.assert_true(len(self.config[module]) > 2)
        try:
            list(raise_if_present(self.config, data))
        except:
            pass
        nt.assert_raises(Exception, "found '100' in 'test'")
