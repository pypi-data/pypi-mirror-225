from conftest import assert_call


def test_run_failure_no_arguments(parser, command_no_arguments, capsys):
    assert_call(parser, "command_test a", """usage: testCommand [-h] {command_test}
testCommand: error: unrecognized arguments: a
""", capsys, exit_code=2)


def test_run_failure_with_arguments(parser, command_with_arguments, capsys):
    assert_call(parser, "command_test a", """usage: testCommand command_test [-h] [--pwd PWD] [--ko KO]
                                [--kwargs KWARGS ...]
                                po pwod [pwd] [args ...]
testCommand command_test: error: the following arguments are required: pwod
""", capsys, exit_code=2)
