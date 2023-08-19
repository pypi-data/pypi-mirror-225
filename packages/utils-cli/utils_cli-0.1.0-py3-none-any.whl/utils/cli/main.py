from typer import Typer

from utils.typer.command import add_command

from .alist.main import app as cmd_alist
from .github.main import app as cmd_github

app: Typer = Typer(name="utils")
add_command(app, command=cmd_alist, name="alist")
add_command(app, command=cmd_github, name="github")
