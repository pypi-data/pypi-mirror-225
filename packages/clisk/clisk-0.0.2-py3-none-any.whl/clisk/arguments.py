from pathlib import Path
from typing import Type, Annotated, Optional

import typer

__all__ = [
    'arg_configuration', 'arg_readable_path', 'arg_writable_path'
]


def arg_readable_path(
        help_message: str = ''
) -> Type[Path]:
    return Annotated[
        Path, typer.Argument(
            help=help_message,
            readable=True
        )
    ]


def arg_writable_path(
        help_message: str = ''
) -> Type[Path]:
    return Annotated[
        Path, typer.Argument(
            help=help_message,
            writable=True
        )
    ]


def arg_configuration(
        help_message: Optional[str] = None
) -> Type[Path]:
    help_message = help_message or 'Path to the configuration file.'
    return Annotated[
        Path, typer.Argument(
            readable=True,
            help=help_message
        )
    ]
