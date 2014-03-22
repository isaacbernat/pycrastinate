import functools


def memoize_last_result_with_params(func):
    func.storage = (None, None, None)

    @functools.wraps(func)
    def memoizer(*args, **kwargs):
        old_args, old_kwargs, old_result = func.storage
        if args == old_args and kwargs == old_kwargs:
            return old_result
        else:
            result = func(*args, **kwargs)
            func.storage = (args, kwargs, result)
            return result
    return memoizer
