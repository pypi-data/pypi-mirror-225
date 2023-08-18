import inspect
from argparse import ArgumentParser, Namespace
from types import ModuleType
from typing import List, Type, TypeVar

from pytoolbelt.toolkit.command import PyToolBeltCommand

CommandModulesType = TypeVar(name="CommandModulesType", bound="CommandModules")


def get_commands(module: ModuleType) -> List[Type[PyToolBeltCommand]]:
    commands = []
    for i, _class in inspect.getmembers(module, inspect.isclass):
        if _class != PyToolBeltCommand:
            if issubclass(_class, PyToolBeltCommand) and not _class.__name__.startswith("Base"):
                commands.append(_class)
    return commands


def parse_args_from_commands(version: str, *modules: ModuleType) -> Namespace:
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    sub_parser.required = True
    parser.add_argument("--version", action="version", version=version)

    for module in modules:
        for command in get_commands(module):
            p = sub_parser.add_parser(command.method(), help=command.help)
            for args, kwargs in command.args.items():
                p.add_argument(*args, **kwargs)
            p.set_defaults(command=command)
    return parser.parse_args()


def parse_args_from_dict(version: str, commands: dict) -> Namespace:
    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    sub_parser.required = True
    parser.add_argument("--version", action="version", version=version)

    for command_name, command in commands.items():
        pass
