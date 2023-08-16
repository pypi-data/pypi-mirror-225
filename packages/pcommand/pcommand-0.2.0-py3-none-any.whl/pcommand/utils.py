from functools import wraps


def decorator(method):
    @wraps(method)
    def decorator_wrapper(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return method(*args, **kwargs)
        else:
            @wraps(method)
            def inner_wrapper(method_):
                return decorator_wrapper(method_, *args, **kwargs)

            return inner_wrapper
    return decorator_wrapper
