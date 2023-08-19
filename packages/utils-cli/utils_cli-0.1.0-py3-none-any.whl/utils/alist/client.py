from pathlib import Path

import requests
from requests import Response

from .response import AuthLoginResponse, FsListResponse

API_URL: str = "https://alist.liblaf.me/api"
CDN_URL: str = "https://cdn.liblaf.me"


class Client:
    api_url: str = API_URL
    token: str

    def __init__(self, api_url: str = API_URL) -> None:
        self.api_url = api_url

    def auth_login(self, username: str, password: str) -> None:
        response: Response = requests.post(
            url=f"{self.api_url}/auth/login",
            json={"username": username, "password": password},
        )
        assert response.ok
        resp: AuthLoginResponse = AuthLoginResponse(**response.json())
        assert resp.ok
        assert resp.data.token
        self.token = resp.data.token

    def fs_list(
        self,
        path: Path,
        *,
        page: int = 1,
        password: str = "",
        per_page: int = 0,
        refresh: bool = False,
    ) -> None:
        response: Response = requests.post(
            url=f"{self.api_url}/fs/list",
            json={
                "page": page,
                "password": password,
                "path": str(path),
                "per_page": per_page,
                "refresh": refresh,
            },
            headers={"Authorization": self.token},
        )
        assert response.ok
        resp: FsListResponse = FsListResponse(**response.json())
        assert resp.ok

    def fs_put(self, data: bytes, file_path: Path, password: str = "") -> None:
        response: Response = requests.put(
            url=f"{self.api_url}/fs/put",
            data=data,
            headers={
                "Authorization": self.token,
                "File-Path": str(file_path),
                "Password": password,
            },
        )
        assert response.ok
        resp: FsListResponse = FsListResponse(**response.json())
        assert resp.ok
