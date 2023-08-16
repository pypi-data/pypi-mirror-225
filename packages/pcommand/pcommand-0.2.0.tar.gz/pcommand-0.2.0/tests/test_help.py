from pcommand import command
from conftest import assert_call


def test_help_no_arguments(parser, command_no_arguments, capsys):
    assert_call(parser, "--help",
                """usage: testCommand [-h] {command_test}

commands:
    command_test

options:
  -h, --help    show this help message and exit
""",
                capsys)

    assert_call(parser, "command_test --help",
                """usage: testCommand command_test [-h]

options:
  -h, --help  show this help message and exit
""",
                capsys)


def test_help_with_arguments(parser, command_with_arguments, capsys):
    assert_call(parser, "--help",
                """usage: testCommand [-h] {command_test}

commands:
    command_test

options:
  -h, --help    show this help message and exit
""",
                capsys)

    assert_call(parser, "command_test --help",
                """usage: testCommand command_test [-h] [--pwd PWD] [--ko KO]
                                [--kwargs KWARGS ...]
                                po pwod [pwd] [args ...]

positional arguments:
  po
  pwod
  pwd
  args

options:
  -h, --help            show this help message and exit
  --pwd PWD
  --ko KO
  --kwargs KWARGS
""", capsys)


def test_help_in_class(parser, command_in_class, capsys):
    assert_call(parser, "--help", """usage: testCommand [-h] {cmd}

commands:
    cmd         Class Help

options:
  -h, --help    show this help message and exit
""", capsys)
    assert_call(parser, "cmd --help", """usage: testCommand cmd [-h] {command_test}

commands:
    command_test

options:
  -h, --help    show this help message and exit
""", capsys)
    assert_call(parser, "cmd command_test --help", """usage: testCommand cmd command_test [-h]

options:
  -h, --help  show this help message and exit
""", capsys)


def test_custom_help(parser, capsys):
    @command(help="Custom help")
    @command.help(po="PO Help", pwod="PWOD Help", pwd="PWD Help", args="ARGS Help", ko="KO Help", kwargs="KWARGS Help")
    def command_test(po, /, pwod, pwd='default_pwd', *args, ko='default_ko', _ko_ignored=None, **kwargs):
        return "command called"

    assert_call(parser, "--help",
                """usage: testCommand [-h] {command_test}

commands:
    command_test
                Custom help

options:
  -h, --help    show this help message and exit
""",
                capsys)

    assert_call(parser, "command_test --help",
                """usage: testCommand command_test [-h] [--pwd PWD] [--ko KO]
                                [--kwargs KWARGS ...]
                                po pwod [pwd] [args ...]

positional arguments:
  po                    PO Help
  pwod                  PWOD Help
  pwd                   PWD Help (default: default_pwd)
  args                  ARGS Help (default: [])

options:
  -h, --help            show this help message and exit
  --pwd PWD             PWD Help (default: default_pwd)
  --ko KO               KO Help (default: default_ko)
  --kwargs KWARGS                        KWARGS Help (default: {})
""", capsys)


def test_help_command_class(parser, command_class, capsys):
    assert_call(parser, "--help", """usage: testCommand [-h] {commandclass}

commands:
    commandclass

options:
  -h, --help    show this help message and exit
""", capsys)
    assert_call(parser, "commandclass --help", """usage: testCommand commandclass [-h] {cmd1,cmd2}

commands:
    cmd1
    cmd2

options:
  -h, --help    show this help message and exit
""", capsys)
    assert_call(parser, "commandclass cmd1 --help", """usage: testCommand commandclass cmd1 [-h]

options:
  -h, --help  show this help message and exit
""", capsys)


def test_run_single_command_class(parser, single_command_class, capsys):
    assert_call(parser, "--help", """usage: testCommand [-h] {singlecommandclass}

commands:
    singlecommandclass

options:
  -h, --help          show this help message and exit
""", capsys)


def test_version(capsys):
    from pcommand import ArgumentParser
    parser = ArgumentParser(prog="testCommand", version="1.2.3")
    assert_call(parser, "-v", "testCommand 1.2.3\n", capsys)
    assert_call(parser, "--version", "testCommand 1.2.3\n", capsys)


def test_type_from_annotation_help(parser, capsys):
    @command
    def command_test(noted_int: int, noted_str: str, noted_bool: bool):
        return noted_int, noted_str, noted_bool

    assert_call(parser, "command_test --help", """usage: testCommand command_test [-h] noted_int noted_str noted_bool

positional arguments:
  noted_int
  noted_str
  noted_bool

options:
  -h, --help  show this help message and exit
""", capsys)
