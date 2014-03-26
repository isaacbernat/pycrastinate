import nose.tools as nt
from modules.exclude import exclude
from datetime import date, timedelta
from mock import patch

data = [
    {'code': u'#TODO write cool sotfware', 'date': date(1988, 1, 14)},
    {'code': u'#TODO celebrate new year', 'date': date(2014, 1, 1)},
    {'code': u'#TODO write more tests', 'date': date(2014, 3, 7)},
]

module = exclude.__name__


class MutableDate(date):
    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


MutableDate.today = classmethod(lambda cls: date(2014, 3, 8))


class TestExclude(object):
    @patch('datetime.date', MutableDate)
    def setup(self):
        from datetime import date
        self.cfg = {module: {
            "date": [{
                "values": [180],
                "functions": [lambda data, value:
                              (data + timedelta(value)) < date.today()],
                }, {
                "values": [15],
                "functions": [lambda data, value:
                              (data + timedelta(value)) >= date.today()],
                }],
            }
        }

    @patch('datetime.date', MutableDate)
    def test_exclude_old_dates(self):
        from datetime import date
        res = list(exclude(self.cfg, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] <
                           timedelta(self.cfg[module]["date"][0]["values"][0]))

    @patch('datetime.date', MutableDate)
    def test_exclude_early_dates(self):
        from datetime import date
        res = list(exclude(self.cfg, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] >
                           timedelta(self.cfg[module]["date"][1]["values"][0]))

    @patch('datetime.date', MutableDate)
    def test_exclude_old_and_early_dates(self):
        """multiple filter tests within a key"""
        from datetime import date
        res = list(exclude(self.cfg, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] <
                           timedelta(self.cfg[module]["date"][0]["values"][0]))
            nt.assert_true(date.today() - r["date"] >
                           timedelta(self.cfg[module]["date"][1]["values"][0]))

    def test_by_default_does_not_exclude(self):
        res = list(exclude({}, data))
        nt.assert_equals(len(res), len(data))

    @patch('datetime.date', MutableDate)
    def test_multiple_keys(self):
        from datetime import date
        del self.cfg[module]["date"][1]
        self.cfg[module]["code"] = [{
            "values": [u'#TODO celebrate'],
            "functions": [lambda data, value: data.startswith(value)]}]
        res = list(exclude(self.cfg, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] <
                           timedelta(self.cfg[module]["date"][0]["values"][0]))
            nt.assert_false(r["code"].startswith("#TODO celebrate"))
