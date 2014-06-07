import nose.tools as nt
from pycrastinate import run

enclose = lambda func, params: func(*params)


class TestPipeline(object):
    def test_all_modules_from_pipeline_are_run(self):
        data = run(self.pipeline, {}, enclose)
        nt.assert_true(5 in data)
        nt.assert_true(50 in data)

    def test_modules_from_pipeline_are_run_in_order(self):
        data = run(self.pipeline, {}, enclose)
        nt.assert_equals(data, [5, 50])

    def plus_5(config, data):
        return data + [5]

    def plus_50(config, data):
        return data + [50]

    pipeline = {
        100: plus_5,
        200: plus_50,
    }


class TestData(object):
    def append_config(config, data):
        return data + [config["append"]]

    pipeline = {100: append_config}

    def test_modules_can_use_config_data(self):
        data = run(self.pipeline, {"append": 5}, enclose)
        nt.assert_true(5 in data)
