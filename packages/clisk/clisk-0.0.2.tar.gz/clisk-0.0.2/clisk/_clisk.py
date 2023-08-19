from __future__ import annotations
from typing import Callable, Union, Any, Sequence, Mapping, MutableMapping, Optional

import typer

__all__ = [
    'KeywordError',
    'Keywords', 'CommandArguments', 'CommandFunction',
    'AppBuilder',
    'command', 'set_up', 'intermediate', 'run'
]


class KeywordError(Exception):
    """Exception raised when the package encounter an error with the command's keywords."""


Keywords = Sequence[str]
CommandArguments = Mapping[str, Any]
CommandFunction = Optional[Callable]


class CommandSet:
    def __init__(self, arguments: CommandArguments):
        self._commands: MutableMapping[str, Union[CommandSet, Command]] = {}
        self._arguments = arguments

    @property
    def children_commands(self) -> Mapping[str, Command]:
        return {k: v for k, v in self._commands.items() if isinstance(v, Command)}

    @property
    def children_commands_set(self) -> Mapping[str, CommandSet]:
        return {k: v for k, v in self._commands.items() if isinstance(v, CommandSet)}

    @property
    def children(self) -> Mapping[str, Union[CommandSet, Command]]:
        return {k: v for k, v in self._commands.items()}

    @property
    def command_argument(self) -> CommandArguments:
        return {k: v for k, v in self._arguments.items()}

    def set_arguments(self, **kwargs):
        self._arguments = kwargs

    def add(self,
            keywords: Keywords,
            function: CommandFunction,
            command_arguments: CommandArguments,
            is_intermediate_command: bool
            ):
        self._check_keywords(keywords)

        if len(keywords) == 1 and is_intermediate_command:
            self._check_intermediate_keyword(keywords[0])
            self._process_intermediate_keyword(keywords[0], command_arguments)
        elif len(keywords) == 1:
            self._check_single_keyword(keywords[0])
            self._process_single_keyword(keywords[0], function, command_arguments)
        else:
            self._check_multiple_keywords(keywords)
            self._process_multiple_keywords(keywords, function, command_arguments, is_intermediate_command)

    def _check_keywords(self, keywords: Keywords):  # NOQA
        if len(keywords) == 0:
            raise KeywordError('A command should have at least one keyword.')

    def _check_multiple_keywords(self, keywords: Keywords):
        if keywords[0] in self._commands and isinstance(self._commands[keywords[0]], Command):
            raise KeywordError(f'The command {keywords} is terminal and cannot contains sub-commands.')

    def _check_single_keyword(self, keyword: str):
        if keyword in self._commands:
            raise KeywordError(f'Multiple usage of the keyword "{keyword}"')

    def _check_intermediate_keyword(self, keyword: str):
        if keyword in self._commands and isinstance(self._commands[keyword], Command):
            raise KeywordError(f'The command {keyword} is terminal and cannot '
                               f'be converted into an intermediate sub-commands.')

    def _process_multiple_keywords(self,
                                   keywords: Keywords,
                                   function: CommandFunction,
                                   command_arguments: CommandArguments,
                                   is_intermediate_command: bool
                                   ):
        if keywords[0] not in self._commands:
            self._commands[keywords[0]] = CommandSet({})
        self._commands[keywords[0]].add(keywords[1:], function, command_arguments, is_intermediate_command)

    def _process_single_keyword(self,
                                keyword: str,
                                function: CommandFunction,
                                command_arguments: CommandArguments
                                ):
        self._commands[keyword] = Command(function, command_arguments)

    def _process_intermediate_keyword(self,
                                      keyword: str,
                                      command_arguments: CommandArguments
                                      ):
        if keyword in self._commands:
            self._commands[keyword]._arguments = command_arguments
        else:
            self._commands[keyword] = CommandSet(command_arguments)


class Command:
    def __init__(self,
                 function: Callable,
                 command_arguments: CommandArguments
                 ):
        self._function = function
        self._command_arguments = command_arguments

    @property
    def function(self) -> Callable:
        return self._function

    @property
    def arguments(self) -> CommandArguments:
        return self._command_arguments


class AppBuilder:
    def __init__(self):
        self._main_command_set = CommandSet({})

    def command(self, *keywords: str, **command_arguments):
        def inner(func):
            self._main_command_set.add(keywords, func, command_arguments, False)
            return func

        return inner

    def intermediate(self, *keywords: str, **command_arguments):
        self._main_command_set.add(keywords, None, command_arguments, True)

    def set_up(self, **command_arguments):
        self._main_command_set.set_arguments(**command_arguments)

    def run(self):
        app = self._build()
        app()

    def _build(self) -> typer.Typer:
        def _build_child(_parent: typer.Typer, _command_set: CommandSet):
            for key, value in _command_set.children_commands.items():
                key: str
                value: Command
                _parent.command(key, **value.arguments)(value.function)

            for key, value in _command_set.children_commands_set.items():
                key: str
                value: CommandSet
                _child = typer.Typer(name=key, **value.command_argument)
                _parent.add_typer(_child)
                _build_child(_child, value)

        main = typer.Typer(**self._main_command_set.command_argument)
        _build_child(main, self._main_command_set)

        return main


default_builder = AppBuilder()
command = default_builder.command
intermediate = default_builder.intermediate
set_up = default_builder.set_up
run = default_builder.run
