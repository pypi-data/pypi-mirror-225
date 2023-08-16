from pcommand import command
from conftest import assert_call


def test_name(parser, capsys):
    @command(name="custom_name")
    def command_test():
        return "custom name"

    assert_call(parser, "--help",
                """usage: testCommand [-h] {custom_name}

commands:
    custom_name

options:
  -h, --help    show this help message and exit
""",
                capsys)

    assert_call(parser, "custom_name", "custom name\n", capsys, expected_exception=None)
