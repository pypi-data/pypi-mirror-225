import inspect
import re
from argparse import ArgumentParser as ArgumentParserBase, SUPPRESS
from collections import defaultdict
from collections.abc import Iterator
from gettext import gettext

from pcommand import HelpAction
from pcommand import HelpFormatter, SubParsersAction


class ArgumentParser(ArgumentParserBase):
    commands = defaultdict(list)
    _subparsers_dict = {}

    def __init__(self, *args, version=None, help_action=HelpAction, **kwargs):
        # Override to add version action if a version value is present
        self.help_action = help_action
        super(ArgumentParser, self).__init__(
            *args, formatter_class=HelpFormatter, exit_on_error=False, **kwargs
        )

        self.subparsers = None

        if version:
            self.add_argument(
                "-v", "--version", action="version", version="%(prog)s " + version
            )

    def parse_args(self, args=None, namespace=None):
        self._add_commands()
        namespace, argv = self.parse_known_args(args, namespace)
        # Print the usage when there is no function to be called
        func = getattr(namespace, 'func', lambda: HelpAction("-h")(self, None, None, "-h"))
        func_args, func_kwargs, argv = ArgumentParser.parse_function_args(func, namespace, argv)

        if argv:
            msg = gettext('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))

        # noinspection PyArgumentList
        resp = func(*func_args, **func_kwargs)
        if resp is not None:
            if isinstance(resp, Iterator):
                resp = list(resp)
            print(resp)
        return namespace

    @staticmethod
    def parse_function_args(func, namespace, argv):
        # Parse the function arguments from namespace to args and kwargs
        func_args = []
        func_kwargs = {}

        for name, info in ArgumentParser.get_method_parameters(func):
            if name.startswith("_"):
                continue

            value = getattr(namespace, name)
            if (
                    info.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
                    and isinstance(value, list)
            ):
                value = value[0]

            if info.kind in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
            ):
                func_args.append(value)
            elif info.kind == inspect.Parameter.VAR_POSITIONAL:
                func_args.extend(value)
            elif info.kind == inspect.Parameter.VAR_KEYWORD:
                value = value.copy()
                var_keywords_regex = r"--(\w+)[ =]?([ \w%\.-]+)?"
                for a in argv[:]:
                    var_keywords = re.search(var_keywords_regex, a)
                    if var_keywords:
                        kw_name, kw_value = var_keywords.groups()
                        value[kw_name] = kw_value
                        argv.remove(a)

                func_kwargs.update(value)
            else:  # info.kind == inspect.Parameter.KEYWORD_ONLY
                func_kwargs[name] = value

        return func_args, func_kwargs, argv

    @staticmethod
    def add_command(command):
        # Add a command in a list to be added as a parameter later
        if command.context:
            context = command.context
        elif command.clazz:
            context = command.clazz.__name__
        else:
            context, _, _ = command.method.__qualname__.split("<locals>.")[-1].rpartition(".")

        commands = ArgumentParser.commands
        if command in commands[context]:
            command_name = (f"{context}." if context else "") + command.name
            print(
                f'WARNING: "{command_name}" already defined. Ignoring...'
            )
        else:
            commands[context].append(command)

    def _add_commands(self):
        # Add the commands as parser parameters
        def get_subparsers(parser_name, clazz=None):
            if parser_name in ArgumentParser._subparsers_dict:
                return ArgumentParser._subparsers_dict[parser_name]

            if parser_name:
                _subparsers = get_subparsers(".".join(f".{parser_name}".split(".")[:-1]))
                if clazz:
                    class_config = {
                        k.replace("_command_", ""): v for k, v in clazz.__dict__.items() if k.startswith("_command_")
                    }
                else:
                    class_config = {}
                class_help = class_config.pop("help", "")
                _parser = _subparsers.add_parser(
                    parser_name.split(".")[-1].lower(), add_help=class_help != SUPPRESS, help=class_help, **class_config
                )
            else:
                _parser = self

            ArgumentParser._subparsers_dict[parser_name] = _parser.add_subparsers(
                title="commands"
            )
            # noinspection PyProtectedMember
            _parser._action_groups.insert(0, _parser._action_groups.pop())
            return get_subparsers(parser_name)

        parsers = self.commands
        while parsers:
            name, commands = parsers.popitem()
            command_class = commands[0].clazz
            subparsers = get_subparsers(name, command_class)
            while commands:
                command = commands.pop(0)
                self._add_parser(command, subparsers)

    @staticmethod
    def _add_parser(command, subparsers):
        help_ = command.kwargs.pop('help')
        config = command.configs
        sub_parser = subparsers.add_parser(
            command.name, add_help=help_ != SUPPRESS, help=help_, **command.kwargs
        )
        sub_parser.set_defaults(func=command.method)
        for name, info in ArgumentParser.get_method_parameters(command.method):
            argument_kwargs = config.get(name, {})
            if info.default != inspect.Parameter.empty:
                argument_kwargs.setdefault("default", info.default)
            if info.annotation != inspect.Parameter.empty:
                argument_kwargs["type"] = info.annotation
            if name.startswith("_"):
                continue
            if info.kind == inspect.Parameter.POSITIONAL_ONLY:
                sub_parser.add_argument(name, nargs=1, **argument_kwargs)
            elif info.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if info.default == inspect.Parameter.empty:
                    sub_parser.add_argument(name, nargs=1, **argument_kwargs)
                else:
                    sub_parser.add_argument(name, nargs="?", **argument_kwargs)
                    sub_parser.add_argument(f"--{name}", nargs=1, **argument_kwargs)
            elif info.kind == inspect.Parameter.VAR_POSITIONAL:
                argument_kwargs["default"] = argument_kwargs.get("default", [])
                sub_parser.add_argument(name, nargs="*", **argument_kwargs)
            elif info.kind == inspect.Parameter.KEYWORD_ONLY:
                if isinstance(info.default, bool):
                    argument_kwargs.pop("type", None)
                    sub_parser.add_argument(f"--{name}", action=f"store_{not info.default}".lower(), **argument_kwargs)
                else:
                    sub_parser.add_argument(f"--{name}", nargs=1, **argument_kwargs)
            elif info.kind == inspect.Parameter.VAR_KEYWORD:
                argument_kwargs["default"] = argument_kwargs.get("default", {})
                sub_parser.add_argument(f"--{name}", nargs="*", **argument_kwargs)

    @staticmethod
    def get_method_parameters(method):
        return inspect.signature(method).parameters.items()

    def _registry_get(self, registry_name, value, default=None):
        # To override the default actions
        if registry_name == "action":
            if value == "help":
                return self.help_action
            if value == "parsers":
                return SubParsersAction
        return self._registries[registry_name].get(value, default)
