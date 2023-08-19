import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Annotated

import typer

from utils.alist.client import API_URL, CDN_URL, Client
from utils.alist.credential import get_password, get_username


def main(
    local_path: Annotated[
        Path,
        typer.Argument(
            exists=True, file_okay=True, dir_okay=False, writable=False, readable=True
        ),
    ],
    remote_prefix: Annotated[
        Path,
        typer.Argument(
            exists=False, file_okay=True, dir_okay=False, writable=False, readable=False
        ),
    ] = Path("/img"),
    *,
    username: Annotated[str, typer.Option("-u", "--username")] = get_username(),
    password: Annotated[str, typer.Option("-p", "--password")] = get_password(),
    api_url: Annotated[str, typer.Option("--api-url", envvar="API_URL")] = API_URL,
    cdn_url: Annotated[str, typer.Option("--cdn-url", envvar="CDN_URL")] = CDN_URL,
) -> None:
    client: Client = Client(api_url=api_url)
    client.auth_login(username=username, password=password)
    remote_path: Path = remote_prefix / (
        datetime.now().strftime("%Y/%m/%d/%Y-%m-%dT%H%M%S") + local_path.suffix
    )
    client.fs_put(data=local_path.read_bytes(), file_path=remote_path)
    client.fs_list(path=remote_path.parent, refresh=True)
    print(urllib.parse.urljoin(cdn_url, str(remote_path)))
