# PyGit

PyGit is a small educational project that shows how a basic Git-like version control system can be built in Python.

It is not a full replacement for Git. Instead, it focuses on the core ideas:

- storing file content as objects
- creating commits
- tracking a simple staging area
- managing branches
- switching branches and merging

## What this project does

This project lets you:

- initialize a repository
- add files to the staging area
- create commits
- check repository status
- create and switch branches
- merge branches
- delete local or remote branches

## Project structure

- [cli.py](cli.py) - command-line interface
- [repository.py](repository.py) - repository operations
- [models.py](models.py) - Git-like object classes such as blob and tree
- [main.py](main.py) - program entry point
- [tests/test_branch_workflow.py](tests/test_branch_workflow.py) - basic workflow test

## How to run

From the project folder, run:

```bash
python main.py init
python main.py add file.txt
python main.py commit -m "first commit"
python main.py status
```

## Useful commands

```bash
python main.py checkout -b feature
python main.py merge main
python main.py branch -d old-branch
python main.py push origin --delete old-branch
```

## Notes

This project is meant for learning and practicing the basic concepts behind Git. It is simple and easy to understand, but it does not include all of Git's advanced features.
