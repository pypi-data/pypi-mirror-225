from typer import Typer

from utils.typer.command import add_command

from .upload import main as cmd_upload

app: Typer = Typer(name="alist")
add_command(app, command=cmd_upload, name="upload")
