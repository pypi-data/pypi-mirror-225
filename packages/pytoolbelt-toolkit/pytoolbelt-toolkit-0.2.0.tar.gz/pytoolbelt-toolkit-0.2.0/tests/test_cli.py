from argparse import Namespace

import pytest

from pytoolbelt.toolkit.command import PyToolBeltCommand


def test_method():
    class MyCommand(PyToolBeltCommand):
        pass

    assert MyCommand.method() == "mycommand"


def test_call():
    class MyCommand(PyToolBeltCommand):
        pass

    command_instance = MyCommand(Namespace())

    with pytest.raises(NotImplementedError):
        command_instance()  # Call the command instance, it should raise NotImplementedError


def test_args():
    class MyCommand(PyToolBeltCommand):
        args = {"--foo": {"help": "Foo help"}}

    assert MyCommand.args == {"--foo": {"help": "Foo help"}}


def test_help():
    class MyCommand(PyToolBeltCommand):
        help = "Some help"

    assert MyCommand.help == "Some help"


def test_multiple_inheritance():
    class MyCommand(PyToolBeltCommand):
        args = {"--foo": {"help": "Foo help"}}

    class MyOtherCommand(MyCommand):
        args = {"--bar": {"help": "Bar help"}}

    assert MyOtherCommand.args == {"--foo": {"help": "Foo help"}, "--bar": {"help": "Bar help"}}


def test_cli():
    class MyCommand(PyToolBeltCommand):
        args = {"--foo": {"help": "Foo help"}}
        help = "Some help"

        def __call__(self) -> None:
            pass

    args = Namespace(command=MyCommand, foo="bar")
    assert MyCommand(args).cli_args == args
