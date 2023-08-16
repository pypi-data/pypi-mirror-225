from argparse import ArgumentError

from conftest import assert_call


def test_run_success_no_arguments(parser, command_no_arguments, capsys):
    assert_call(parser, "", "usage: testCommand [-h] {command_test}\n", capsys)
    assert_call(parser, "command_test", "command called\n", capsys, expected_exception=None)


def test_run_success_with_arguments(parser, command_with_arguments, capsys):
    assert_call(parser, "", "usage: testCommand [-h] {command_test}\n", capsys)
    assert_call(parser, "command_test PO PWOD",
                "command called with PO, PWOD, default_pwd, default_ko, (), {}\n",
                capsys, expected_exception=None)
    assert_call(parser, "command_test PO PWOD PWD ARG1 ARG2 --ko=KO --kw1=KW2",
                "command called with PO, PWOD, PWD, KO, ('ARG1', 'ARG2'), {'kw1': 'KW2'}\n",
                capsys, expected_exception=None)
    assert_call(parser, "command_test PO PWOD --pwd=PWD",
                "command called with PO, PWOD, PWD, default_ko, (), {}\n",
                capsys, expected_exception=None)


def test_run_in_class(parser, command_in_class, capsys):
    assert_call(parser, "cmd", "usage: testCommand [-h] {cmd}\n", capsys)
    assert_call(parser, "command_test", "argument {cmd}: invalid choice: 'command_test' (choose from 'cmd')", capsys,
                expected_exception=ArgumentError)
    assert_call(parser, "cmd command_test", "command in class\n", capsys, expected_exception=None)


def test_run_command_class(parser, command_class, capsys):
    assert_call(parser, "commandclass cmd1", "cmd1\n", capsys, expected_exception=None)


def test_run_single_command_class(parser, single_command_class, capsys):
    assert_call(parser, "singlecommandclass singlecmd", "singlecmd\n", capsys, expected_exception=None)
    assert_call(
        parser,
        "singlecommandclass ignoredcmd",
        "argument {singlecmd}: invalid choice: 'ignoredcmd' (choose from 'singlecmd')",
        capsys,
        expected_exception=ArgumentError
    )
    from pcommand import command
    command(single_command_class.ignoredcmd)
    assert_call(parser, "singlecommandclass ignoredcmd", "ignoredcmd\n", capsys, expected_exception=None)


def test_return_list(parser, capsys):
    from pcommand import command

    @command
    def command_test():
        for x in range(3):
            yield x

    assert_call(parser, "command_test", "[0, 1, 2]\n", capsys, expected_exception=None)


def test_run_command_context(parser, capsys):
    from pcommand import command

    @command(context="commandcontext")
    def ctxcmd1():
        print("ctxcmd1")

    assert_call(parser, "commandcontext ctxcmd1", "ctxcmd1\n", capsys, expected_exception=None)


def test_run_bool_as_default(parser, capsys):
    from pcommand import command

    @command
    def command_test(*, bool_arg: bool = True):
        print(bool_arg)

    assert_call(parser, "command_test", "True\n", capsys, expected_exception=None)
