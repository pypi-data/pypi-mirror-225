import argparse
from typing import Optional, List, Dict, Any, Callable, Union, Tuple


class entrypoint:
    _commands = {}
    _command_flags = {}
    _command_help = {}
    _global_flags = []  # Store global flags

    def __init__(self, *, command: Optional[str] = None, flags: Optional[List[Dict]] = None, help_msg: Optional[str] = None) -> None:
        self.command_name = command
        self.flags = flags or []
        self.help_msg = help_msg
        self._is_default = command is None  # This attribute helps distinguish default from other commands

    def __call__(self, func):
        # If command_name is None, it's a default function
        if self._is_default:
            self._commands["default"] = func
        else:
            self._commands[self.command_name] = func
            self._command_flags[self.command_name] = self.flags
            self._command_help[self.command_name] = self.help_msg
        return func

    @classmethod
    def build_parser(cls, version: str, tool_description: str) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=tool_description)
        parser.add_argument("--version", action="version", version=version)

        # Add global flags
        for arg_data in cls._global_flags:
            parser.add_argument(arg_data.pop("name"), **arg_data)

        subparsers = parser.add_subparsers(title='commands', dest='command')

        for cmd, func in cls._commands.items():
            if cmd == "default":  # Skip default for sub-commands
                continue
            command_parser = subparsers.add_parser(cmd, help=cls._command_help.get(cmd))
            for arg_data in cls._command_flags.get(cmd, []):
                command_parser.add_argument(arg_data.pop("name"), **arg_data)

        return parser

    @classmethod
    def run(cls, args):
        if args.command and args.command in cls._commands:
            return cls._commands[args.command](cli_args=args)
        else:
            # Run default function if no sub-command is specified
            if "default" in cls._commands:
                return cls._commands["default"](cli_args=args)
        return 1  # Return an error code if no suitable command or default is found

    @classmethod
    def set_global_flags(cls, flags):
        cls._global_flags.extend(flags)

    @staticmethod
    def execute(version: Optional[str] = None, tool_description: Optional[str] = None) -> None:

        if not version:
            version = "0.0.0"

        if not tool_description:
            tool_description = "A tool built with pytoolbelt toolkit."

        parser = entrypoint.build_parser(version=version, tool_description=tool_description)
        args = parser.parse_args()
        exit_code = entrypoint.run(args)
        exit(exit_code)
