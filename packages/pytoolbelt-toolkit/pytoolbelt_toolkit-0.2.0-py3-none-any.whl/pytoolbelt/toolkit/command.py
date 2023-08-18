from argparse import Namespace
from typing import TypeVar

CommandType = TypeVar("CommandType", bound="Command")


class _CommandMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Merging 'args' dictionaries of parent classes and the new class
        new_args = {}
        for base in reversed(bases):
            if hasattr(base, "args"):
                new_args.update(base.args)
        if "args" in attrs:
            new_args.update(attrs["args"])
        attrs["args"] = new_args

        return super().__new__(mcs, name, bases, attrs)


class PyToolBeltCommand(metaclass=_CommandMeta):
    args = {}
    help = ""

    def __init__(self, cli_args: Namespace) -> None:
        self.cli_args = cli_args

    @classmethod
    def method(cls) -> str:
        return cls.__name__.lower()

    def __call__(self) -> None:
        raise NotImplementedError
