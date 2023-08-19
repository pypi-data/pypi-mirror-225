from typer import Typer

from utils.typer.command import add_command

from .clone import main as cmd_clone

app: Typer = Typer(name="github")
add_command(app, command=cmd_clone, name="clone")
