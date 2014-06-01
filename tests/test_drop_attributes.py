import nose.tools as nt
from modules.drop_attributes import drop_attributes
module = drop_attributes.__name__


class TestDropAttributes(object):
    def setup(self):
        self.data = [
            {'code': u'#TODO write cool sotfware', 'token': 'TODO'},
            {'code': u'#FIXME celebrate new year', 'token': 'FIXME'},
            {'code': u'#todo write more tests', 'token': 'todo', 'test': 100},
        ]
        self.config = {module: {}, }

    def test_doesnt_drop_attrs_by_default(self):
        res = list(drop_attributes(self.config, self.data))
        nt.assert_equals(res, self.data)

    def test_drops_attrs_in_list(self):
        self.config[module] = {"attr_list": ["code"]}
        for d in self.data:
            nt.assert_true("code" in d)
        res = list(drop_attributes(self.config, self.data))
        for r in res:
            nt.assert_true("code" not in r)

    def test_only_drops_attrs_in_list(self):
        self.config[module] = {"attr_list": ["code"]}
        res = list(drop_attributes(self.config, self.data))
        for r in res:
            nt.assert_true("token" in r)

    def test_doesnt_crash_if_dict_doesnt_have_attr(self):
        self.config[module] = {"attr_list": ["test"]}
        res = list(drop_attributes(self.config, self.data))
        for r in res:
            nt.assert_true("test" not in r)

    def test_drop_multiple_attrs(self):
        self.config[module] = {"attr_list": ["code", "token"]}
        res = list(drop_attributes(self.config, self.data))
        for r in res:
            nt.assert_true("token" not in r)
            nt.assert_true("code" not in r)

    def test_lines_are_deleted_if_empty_dicts(self):
        self.config[module] = {"attr_list": ["code", "token"]}
        res = list(drop_attributes(self.config, self.data))
        nt.assert_equals(len(res), 1)
