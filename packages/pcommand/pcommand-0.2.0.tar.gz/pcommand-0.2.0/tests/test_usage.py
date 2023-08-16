from conftest import assert_call


def test_usage_no_arguments(parser, command_no_arguments, capsys):
    assert_call(parser, "-h", "usage: testCommand [-h] {command_test}\n", capsys)
    assert_call(parser, "command_test -h", "usage: testCommand command_test [-h]\n", capsys)


def test_usage_with_arguments(parser, command_with_arguments, capsys):
    assert_call(parser, "-h", "usage: testCommand [-h] {command_test}\n", capsys)
    assert_call(parser, "command_test -h",
                """usage: testCommand command_test [-h] [--pwd PWD] [--ko KO]
                                [--kwargs KWARGS ...]
                                po pwod [pwd] [args ...]
""", capsys)


def test_usage_in_class(parser, command_in_class, capsys):
    assert_call(parser, "-h", "usage: testCommand [-h] {cmd}\n", capsys)
    assert_call(parser, "cmd -h", "usage: testCommand cmd [-h] {command_test}\n", capsys)
    assert_call(parser, "cmd command_test -h", "usage: testCommand cmd command_test [-h]\n", capsys)
