import subprocess


def push(remote, branch=None, delete=False):
    command = ["git", "push", remote]

    if delete:
        command.extend(["--delete", branch])
    elif branch:
        command.append(branch)

    subprocess.run(command, check=True)
