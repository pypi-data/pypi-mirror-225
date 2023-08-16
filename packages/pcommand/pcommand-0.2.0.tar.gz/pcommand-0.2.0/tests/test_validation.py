from conftest import assert_call


def test_same_command_name_warning(parser, capsys):
    from pcommand import command

    @command
    def cmd():
        pass

    @command(name="cmd")
    def cmd2():
        pass

    assert_call(parser, "cmd", "WARNING: \"cmd\" already defined. Ignoring...\n", capsys, expected_exception=None)
