import json
import subprocess
from collections.abc import Iterable
from pathlib import Path
from subprocess import CompletedProcess, Popen
from typing import Annotated

import typer


def repo_list() -> Iterable[str]:
    process: CompletedProcess = subprocess.run(
        args=[
            "gh",
            "repo",
            "list",
            "--json=nameWithOwner",
            "--limit=1000",
            "--no-archived",
            "--source",
        ],
        capture_output=True,
        check=True,
    )
    return map(lambda repo: repo["nameWithOwner"], json.loads(process.stdout))


def main(
    *,
    prefix: Annotated[
        Path,
        typer.Option(
            "-p",
            "--prefix",
            exists=False,
            file_okay=False,
            dir_okay=True,
            writable=True,
            readable=False,
        ),
    ] = Path.home()
    / "Desktop"
    / "github"
) -> None:
    processes: Iterable[Popen] = list(
        map(
            lambda repo: Popen(
                args=[
                    "gh",
                    "repo",
                    "clone",
                    repo,
                    prefix / repo,
                    "--",
                    "--recurse-submodules",
                    "--remote-submodules",
                ]
            ),
            repo_list(),
        )
    )
    for process in processes:
        process.wait()
