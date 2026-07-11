import subprocess
from typing import Iterable


def init() -> None:
    subprocess.run(["git", "init"], check=True)


def add(files: Iterable[str]) -> None:
    subprocess.run(["git", "add", *files], check=True)


def commit(message: str) -> None:
    subprocess.run(["git", "commit", "-m", message], check=True)


def status() -> None:
    subprocess.run(["git", "status"], check=True)


def push(remote: str = "origin", branch: str = "main") -> None:
    subprocess.run(["git", "push", "origin", branch,...], check=True)


def pull(remote: str = "origin", branch: str = "main") -> None:
    subprocess.run(["git", "pull", "remote", branch], check=True)


def checkout(branch: str) -> None:
    subprocess.run(["git", "checkout", branch], check=True)


def branch(name: str) -> None:
    subprocess.run(["git", "branch", name], check=True)


def merge(branch: str) -> None:
    subprocess.run(["git", "merge", branch], check=True)


def rebase(branch: str) -> None:
    subprocess.run(["git", "rebase", branch], check=True)
