import inspect
from collections import defaultdict

from pcommand.utils import decorator


# noinspection PyPep8Naming
class Command:
    _methods = defaultdict(dict)

    def __init__(self, method, args, kwargs):
        self.method = method
        self.args = args
        self.context = kwargs.pop("context", None)
        self.name = kwargs.pop("name", self.method.__name__)
        self.kwargs = kwargs
        if not isinstance(kwargs.get("aliases", []), list):
            kwargs["aliases"] = [kwargs["aliases"]]
        self.kwargs.setdefault("help", "")
        self.configs = Command._methods.get(method, {})

    def __eq__(self, other):
        return self.name == other.name

    @property
    def clazz(self):
        method = self.method
        # if inspect.ismethod(method):
        #     for cls in inspect.getmro(method.__self__.__class__):
        #         if cls.__dict__.get(method.__name__) is method:
        #             return cls
        #     method = method.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(method):
            try:
                cls = getattr(inspect.getmodule(method),
                              method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
                if isinstance(cls, type):
                    return cls
            except AttributeError:
                pass
        return getattr(method, '__objclass__', None)


class _CommandDecorator:

    @staticmethod
    @decorator
    def __call__(method, *args, **kwargs):
        from pcommand import ArgumentParser
        if isinstance(method, type):
            clazz = method
            for _, method_ in inspect.getmembers(
                    clazz,
                    predicate=lambda m: inspect.isfunction(m) and not m.__name__.startswith('_')
            ):
                ArgumentParser.add_command(Command(method_, args, kwargs.copy()))
            return clazz
        else:
            ArgumentParser.add_command(Command(method, args, kwargs))
            return method

    def __getattr__(self, item):
        if item.startswith("_"):
            raise AttributeError("command", item)

        def _config_wrapper(method, **config):
            return _CommandDecorator._config(method, item, **config)

        return decorator(_config_wrapper)

    # noinspection PyProtectedMember
    @staticmethod
    def _config(method, config_name, **config):
        for arg, conf in config.items():
            Command._methods[method][arg] = {config_name: conf}

        return method


command = _CommandDecorator()
