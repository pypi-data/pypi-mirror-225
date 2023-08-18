import argparse
from typing import Any, Callable, Dict, List, Optional, TypeVar

T = TypeVar("T", bound=Callable[..., Any])

# Custom type aliases
CommandData = Dict[str, Any]
CommandDict = Dict[str, CommandData]
FlagDict = Dict[str, Any]


class entrypoint:
    _commands: CommandDict = {}
    _global_flags: List[FlagDict] = []

    def __init__(
        self, *, command: Optional[str] = None, flags: Optional[List[FlagDict]] = None, help_msg: Optional[str] = None
    ) -> None:
        self.command_data: CommandData = {"func": None, "flags": flags or [], "help_msg": help_msg}
        self.command_name: str = command or "default"

    def __call__(self, func: T) -> T:
        self.command_data["func"] = func
        self._commands[self.command_name] = self.command_data
        return func

    @classmethod
    def build_parser(cls, version: str, tool_description: str) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=tool_description)
        parser.add_argument("--version", action="version", version=version)

        for arg_data in cls._global_flags:
            parser.add_argument(arg_data.pop("name"), **arg_data)

        subparsers = parser.add_subparsers(title="commands", dest="command")
        for cmd, data in cls._commands.items():
            if cmd == "default":  # Skip default for sub-commands
                continue
            command_parser = subparsers.add_parser(cmd, help=data.get("help_msg"))
            for arg_data in data.get("flags", []):
                command_parser.add_argument(arg_data.pop("name"), **arg_data)

        return parser

    @classmethod
    def run(cls, args: argparse.Namespace) -> int:
        func = cls._commands.get(args.command or "default", {}).get("func")
        if func:
            return func(cli_args=args)
        return 1  # Return an error code if no suitable command or default is found

    @classmethod
    def set_global_flags(cls, flags: List[FlagDict]) -> None:
        cls._global_flags.extend(flags)

    @staticmethod
    def execute(
        version: Optional[str] = "0.0.0", tool_description: Optional[str] = "A tool built with pytoolbelt toolkit."
    ) -> None:
        parser = entrypoint.build_parser(version=version, tool_description=tool_description)
        args = parser.parse_args()
        exit_code = entrypoint.run(args)
        exit(exit_code)
