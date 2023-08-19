from pathlib import Path
from typing import Type, Annotated, Callable, Optional

import typer

__all__ = [
    'set_verbose_callback', 'opt_verbosity',
    'opt_configuration', 'opt_readable_path', 'opt_writable_path'
]

verbose_callback = None


def set_verbose_callback(callback: Callable[[int], ...]):
    global verbose_callback
    verbose_callback = callback


def opt_verbosity() -> Type[int]:
    return Annotated[int, typer.Option(
        '--verbose', '-v',
        callback=verbose_callback,
        count=True,
        help='Increase the log verbosity',
        is_eager=True
    )]


def opt_readable_path(
        *names: str,
        help_message: str = ''
) -> Type[Path]:
    if len(names) == 0:
        raise KeyError('A path option must have at least one name.')

    return Annotated[
        Path, typer.Option(
            *names,
            help=help_message,
            readable=True
        )
    ]


def opt_writable_path(
        *names: str,
        help_message: str = ''
) -> Type[Path]:
    if len(names) == 0:
        raise KeyError('A path option must have at least one name.')

    return Annotated[
        Path, typer.Option(
            *names,
            help=help_message,
            writable=True
        )
    ]


def opt_configuration(
        *names: str,
        help_message: Optional[str] = None
) -> Type[Path]:
    if len(names) == 0:
        names = ('--configuration', '-c')

    help_message = help_message or 'Path to the configuration file.'
    return Annotated[
        Path, typer.Option(
            *names,
            readable=True,
            help=help_message
        )
    ]
