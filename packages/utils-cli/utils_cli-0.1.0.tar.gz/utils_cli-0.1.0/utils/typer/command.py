from typing import Callable, Optional

from typer import Typer


def add_command(app: Typer, command: Callable, name: Optional[str] = None) -> None:
    if isinstance(command, Typer):
        app.add_typer(command, name=name)
    else:
        app.command(name=name)(command)
