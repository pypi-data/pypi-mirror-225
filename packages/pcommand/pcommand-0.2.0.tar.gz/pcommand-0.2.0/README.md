# PCommand
[![Tests](https://github.com/heitorpolidoro/polidoro-command/actions/workflows/push.yml/badge.svg)](https://github.com/heitorpolidoro/polidoro-command/actions/workflows/push.yml)
![GitHub last commit](https://img.shields.io/github/last-commit/heitorpolidoro/polidoro-command)
[![Coverage Status](https://coveralls.io/repos/github/heitorpolidoro/polidoro-command/badge.svg?branch=master)](https://coveralls.io/github/heitorpolidoro/polidoro-command?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=heitorpolidoro_polidoro-command&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=heitorpolidoro_polidoro-command)

[![Latest](https://img.shields.io/github/release/heitorpolidoro/polidoro-command.svg?label=latest)](https://github.com/heitorpolidoro/polidoro-command/releases/latest)
![GitHub Release Date](https://img.shields.io/github/release-date/heitorpolidoro/polidoro-command)

![PyPI - Downloads](https://img.shields.io/pypi/dm/polidoro-command?label=PyPi%20Downloads)

![GitHub](https://img.shields.io/github/license/heitorpolidoro/polidoro-command)

Package to simplify creating command line arguments for scripts in Python.

#### How to use:

- Decorate the method you want to call from command line with `@command`.
- Create a `PolidoroArgumentParser`
- Call `parser.parse_args()`

All keywords arguments to `@command` are the same as in [argparse.ArgumentParser.add_argument](https://docs.python.org/3.7/library/argparse.html#the-add-argument-method) except for 'action' and 'nargs' 
which is calculated based on the method signature.

To create commands

```python
from pcommand import PolidoroArgumentParser, command


@command
def cool_command():
    print('this is a command')
    
PolidoroArgumentParser().parse_args()
# OR
parser = PolidoroArgumentParser()
parser.parse_args()
```
```bash
$ python foo.py --help
usage: testCommand [-h] {cool_command}

commands:
    cool_command

options:
  -h, --help    show this help message and exit
  
$ python foo.py cool_command
this is a command
```
With arguments

```python
@command
def command_with_arg(arg1, arg2=None):
    print(f"this the command arg1: {arg1}, arg2: {arg2}")
```
```bash
$ python foo.py command_with_arg --help
usage: testCommand command_with_arg [-h] [--arg2 ARG2] arg1

positional arguments:
  arg1

options:
  -h, --help   show this help message and exit
  --arg2 ARG2
  
$ python foo.py command_with_arg Hello
this the command arg: Hello, arg1: None

$ python foo.py command_with_arg Hello --arg1 World
this the command arg: Hello, arg1: World
```

Using a Class
```python
class ClassCommand:
    @staticmethod
    @command
    def command_in_class(arg='Oi'):
        print(f"command_in_class called. arg={arg}")
```
```bash
$ python foo.py classcommand command_in_class
command_in_class called. arg=Oi

$ python foo.py classcommand command_in_class --arg=Ola
command_in_class called. arg=Ola
```

Adding help
```python
@command(help="command help", config={
    "arg1": {"help": "Arg1 Help"},
    "arg2": {"help": "Arg2 Help"},
})
def command_with_arg(arg1, *, arg2=None):
    print(f"this the command arg1: {arg1}, arg2: {arg2}")
```
```bash
$ python foo.py command_with_arg --help
usage: testCommand command_with_arg [-h] [--arg2 ARG2] arg1

positional arguments:
  arg1         Arg1 Help

options:
  -h, --help   show this help message and exit
  --arg2 ARG2  Arg2 Help (default: None)
```

How the parameter kind is parser to argument type:

| Parameter Kind                               | Argument type                                                                                                                                        |
|----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| POSITIONAL_ONLY                              | Positional argument (required, nargs=1)                                                                                                              |
| POSITIONAL_OR_KEYWORD <br> (without default) | Positional argument (required, nargs=1)                                                                                                              |
| POSITIONAL_OR_KEYWORD <br> (with default)    | Positional argument (optional, nargs="?", default=default in signature) <br> and optional argument (required, nargs=1, default=default in signature) |
| VAR_POSITIONAL                               | Positional argument (optional, nargs="*", default=[])                                                                                                |
| KEYWORD_ONLY                                 | Optional argument (required, nargs=1, default=default in signature)                                                                                  |
| VAR_KEYWORD                                  | Optional argument (optional, nargs="*", default={})                                                                                                  |

[For mor information about parameters kinds](https://docs.python.org/3/library/inspect.html#inspect.Parameter.kind)