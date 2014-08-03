import nose.tools as nt
from modules.filter_by_age import filter_by_age
from datetime import date, timedelta
from mock import patch

data = [
    {'code': u'#TODO write cool sotfware', 'date': date(1988, 1, 14)},
    {'code': u'#TODO celebrate new year', 'date': date(2014, 1, 1)},
    {'code': u'#TODO write more tests', 'date': date(2014, 3, 7)},
]

module = filter_by_age.__name__

config = {module: {
    "oldest": 180,
    "earliest": 15,
    }
}


class MutableDate(date):
    def __new__(cls, *args, **kwargs):
        return date.__new__(date, *args, **kwargs)


MutableDate.today = classmethod(lambda cls: date(2014, 3, 8))


class TestFilterByAge(object):
    @patch('datetime.date', MutableDate)
    def test_filter_old_dates(self):
        from datetime import date
        res = list(filter_by_age(config, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] <
                           timedelta(config[module]["oldest"]))

    @patch('datetime.date', MutableDate)
    def test_filter_early_dates(self):
        from datetime import date
        res = list(filter_by_age(config, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] >
                           timedelta(config[module]["earliest"]))

    @patch('datetime.date', MutableDate)
    def test_filter_old_and_early_dates(self):
        from datetime import date
        res = list(filter_by_age(config, data))
        nt.assert_true(len(res) > 0)
        for r in res:
            nt.assert_true(date.today() - r["date"] <
                           timedelta(config[module]["oldest"]))
            nt.assert_true(date.today() - r["date"] >
                           timedelta(config[module]["earliest"]))

    @patch('datetime.date', MutableDate)
    def test_by_default_does_not_filter(self):
        res = list(filter_by_age({}, data))
        nt.assert_equals(len(res), len(data))
