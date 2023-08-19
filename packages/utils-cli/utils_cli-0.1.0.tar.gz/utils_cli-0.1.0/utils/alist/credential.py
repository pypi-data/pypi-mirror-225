import subprocess
from subprocess import CompletedProcess

BITWARDEN_ID: str = "914c8b9a-c3cd-4c10-b3b6-b00100d34c67"


def get_username() -> str:
    try:
        process: CompletedProcess = subprocess.run(
            args=["bw", "get", "username", BITWARDEN_ID],
            capture_output=True,
            check=True,
        )
        stdout: bytes = process.stdout
        return stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ""


def get_password() -> str:
    try:
        process: CompletedProcess = subprocess.run(
            args=["bw", "get", "password", BITWARDEN_ID],
            capture_output=True,
            check=True,
        )
        stdout: bytes = process.stdout
        return stdout.decode().strip()
    except subprocess.CalledProcessError:
        return ""
