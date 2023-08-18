import argparse

import pytest

from pytoolbelt.toolkit.decorators import entrypoint


@pytest.fixture(autouse=True)
def cleanup_entrypoint():
    yield
    entrypoint._global_flags.clear()
    entrypoint._commands.clear()


def test_command_registration():
    @entrypoint(command="test_cmd", flags=[{"name": "--option", "type": str}], help_msg="Test command")
    def test_func(cli_args):
        return 0

    assert "test_cmd" in entrypoint._commands
    assert entrypoint._commands["test_cmd"]["help_msg"] == "Test command"
    assert entrypoint._commands["test_cmd"]["flags"] == [{"name": "--option", "type": str}]


def test_global_flags():
    flags = [{"name": "--global_option", "type": str}]
    entrypoint.set_global_flags(flags)

    assert flags[0] in entrypoint._global_flags


def test_parser_building():
    version = "1.0.0"
    tool_description = "Test tool description"
    parser = entrypoint.build_parser(version, tool_description)

    # Not a comprehensive test; just a simple check to see if the version and tool description are set correctly.
    assert parser.description == tool_description
    assert any(action for action in parser._actions if action.dest == "version" and action.version == version)


def test_execution():
    @entrypoint(command="execute_test")
    def foo_func(cli_args):
        return 0

    # Note: This isn't the best test because it doesn't actually run the execute() method, but it gives you an idea.
    # Ideally, you'd use a library like `unittest.mock` to mock out sys.argv and see if the command is executed correctly.
    args = argparse.Namespace(command="execute_test")
    exit_code = entrypoint.run(args)

    assert exit_code == 0


def test_default_command_registration():
    @entrypoint()
    def default_func(cli_args):
        return 0

    assert "default" in entrypoint._commands
    assert entrypoint._commands["default"]["func"] == default_func


def test_run_command_with_flags():
    flag_value = "sample_value"

    @entrypoint(command="flag_test_cmd", flags=[{"name": "--flag", "type": str}])
    def flag_test_func(cli_args):
        return 0 if cli_args.flag == flag_value else 1

    class MockArgs:
        command = "flag_test_cmd"
        flag = flag_value

    assert entrypoint.run(MockArgs()) == 0

    MockArgs.flag = "wrong_value"
    assert entrypoint.run(MockArgs()) == 1


def test_run_default_command():
    @entrypoint()
    def default_func(cli_args):
        return 0

    class MockArgs:
        command = None

    assert entrypoint.run(MockArgs()) == 0


def test_run_non_existent_command():
    class MockArgs:
        command = "i_dont_exist"

    assert entrypoint.run(MockArgs()) == 1
