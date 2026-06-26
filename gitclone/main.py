from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
import time
import zlib
from pathlib import Path

logging.getLogger().setLevel(logging.CRITICAL)


class Gitobject:
    def __init__(self, obj_type: str, content: bytes):
        self.type = obj_type
        self.content = content

    def hash(self) -> str:
        header = f"{self.type} {len(self.content)}\0".encode()
        return hashlib.sha1(header + self.content).hexdigest()

    def serialize(self) -> bytes:
        header = f"{self.type} {len(self.content)}\0".encode()
        return zlib.compress(header + self.content)

    @classmethod
    def deserialize(cls, data: bytes) -> "Gitobject":
        decompress = zlib.decompress(data)
        null_id = decompress.find(b"\0")
        header = decompress[:null_id]
        content = decompress[null_id + 1 :]
        obj_type, _ = header.split(b" ", 1)
        return cls(obj_type.decode(), content)


class Blob(Gitobject):
    def __init__(self, content: bytes):
        super().__init__("blob", content)


class Tree(Gitobject):
    def __init__(self, entries: list[tuple[str, str, str]] | None = None):
        self.entries = entries or []
        content = self._serialize_entries()
        super().__init__("tree", content)

    def _serialize_entries(self) -> bytes:
        content = b""
        for name, mode, obj_hash in sorted(
            self.entries, key=lambda entry: (entry[1], entry[0])
        ):
            content += f"{mode} {name}\0".encode()
            content += bytes.fromhex(obj_hash)
        return content

    def add_entries(self, name: str, mode: str, obj_hash: str):
        self.entries.append((name, mode, obj_hash))

    @classmethod
    def from_content(cls, content: bytes) -> "Tree":
        tree = cls([])
        i = 0
        while i < len(content):
            null_index = content.find(b"\0", i)
            if null_index == -1:
                break
            mode_name = content[i:null_index].decode()
            mode, name = mode_name.split(" ", 1)
            obj_hash = content[null_index + 1 : null_index + 21].hex()
            tree.entries.append((name, mode, obj_hash))
            i = null_index + 21
        return tree


class repository:
    def __init__(self, path: str | None = None):
        self.path = Path(path).resolve() if path else Path.cwd().resolve()
        self.git_dir = self.path / ".pygit"
        self.object_dir = self.git_dir / "objects"
        self.ref_dir = self.git_dir / "refs"
        self.head_file = self.git_dir / "HEAD"
        self.index_file = self.git_dir / "index"
        self.heads_dir = self.ref_dir / "heads"

    def init(self):
        self.git_dir.mkdir(exist_ok=True)
        self.object_dir.mkdir(exist_ok=True)
        self.ref_dir.mkdir(exist_ok=True)
        self.heads_dir.mkdir(exist_ok=True)
        self.head_file.write_text("ref: refs/heads/main\n", encoding="utf-8")
        self._write_ref("main", "")
        self.save_index({})
        print(f"Initialized empty pygit repository in {self.git_dir}")
        return True

    def load_index(self) -> dict[str, str]:
        if not self.index_file.exists():
            return {}
        try:
            return json.loads(self.index_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def save_index(self, index: dict[str, str]):
        self.index_file.write_text(json.dumps(index, indent=2), encoding="utf-8")

    def store_object(self, obj: Gitobject) -> str:
        obj_hash = obj.hash()
        object_dir = self.object_dir / obj_hash[:2]
        object_file = object_dir / obj_hash[2:]
        if not object_file.exists():
            object_dir.mkdir(exist_ok=True)
            object_file.write_bytes(obj.serialize())
        return obj_hash

    def _ref_path(self, branch: str) -> Path:
        return self.heads_dir / branch

    def _read_ref(self, branch: str) -> str:
        ref_file = self._ref_path(branch)
        if not ref_file.exists():
            return ""
        return ref_file.read_text(encoding="utf-8").strip()

    def _write_ref(self, branch: str, value: str):
        self._ref_path(branch).write_text(value, encoding="utf-8")

    def get_current_branch(self) -> str:
        if not self.head_file.exists():
            return "main"
        head = self.head_file.read_text(encoding="utf-8").strip()
        if head.startswith("ref: refs/heads/"):
            return head.split("/")[-1]
        return "HEAD"

    def _get_head_ref(self) -> str:
        if not self.head_file.exists():
            return ""
        head = self.head_file.read_text(encoding="utf-8").strip()
        if head.startswith("ref: "):
            return head[5:].strip()
        return ""

    def add_file(self, path: str):
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found")
        content = full_path.read_bytes()
        blob = Blob(content)
        blob_hash = self.store_object(blob)
        index = self.load_index()
        index[path] = blob_hash
        self.save_index(index)
        print(f"Added {path}")
        return blob_hash

    def add_dir(self, path: str):
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found")
        for file_path in full_path.rglob("*"):
            if self.git_dir in file_path.parents:
                continue
            if file_path.is_file():
                rel_path = file_path.relative_to(self.path).as_posix()
                self.add_file(rel_path)

    def add_path(self, path: str) -> None:
        full_path = self.path / path
        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found")
        if full_path.is_file():
            self.add_file(path)
        elif full_path.is_dir():
            self.add_dir(path)
        else:
            raise ValueError(f"{path} is found in file and folder")

    def create_tree_from_index(self) -> str:
        index = self.load_index()
        tree_entries: dict[str, object] = {}
        for path, blob_hash in sorted(index.items()):
            current = tree_entries
            parts = path.split("/")
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = blob_hash
        return self._build_tree(tree_entries)

    def _build_tree(self, node: dict[str, object]) -> str:
        tree = Tree([])
        for name in sorted(node):
            value = node[name]
            if isinstance(value, dict):
                obj_hash = self._build_tree(value)
                tree.add_entries(name, "40000", obj_hash)
            else:
                tree.add_entries(name, "100644", value)
        return self.store_object(tree)

    def get_head_commit_hash(self) -> str:
        branch = self.get_current_branch()
        return self._read_ref(branch)

    def read_object(self, obj_hash: str):
        object_file = self.object_dir / obj_hash[:2] / obj_hash[2:]
        if not object_file.exists():
            raise FileNotFoundError(f"Object {obj_hash} not found")
        return Gitobject.deserialize(object_file.read_bytes())

    def commit(self, message: str, author: str = "PyGituser <user@pygit.com>") -> str:
        tree_hash = self.create_tree_from_index()
        parent_hash = self.get_head_commit_hash() if self.get_head_commit_hash() else ""
        timestamp = int(time.time())
        lines = [f"tree {tree_hash}"]
        if parent_hash:
            lines.append(f"parent {parent_hash}")
        lines.extend(
            [
                f"author {author} {timestamp} +0000",
                f"committer {author} {timestamp} +0000",
                "",
                message,
            ]
        )
        commit_obj = Gitobject("commit", "\n".join(lines).encode("utf-8"))
        commit_hash = self.store_object(commit_obj)
        branch = self.get_current_branch()
        self._write_ref(branch, commit_hash)
        print(f"[{branch}] {message}")
        return commit_hash

    def branch(self, name: str) -> str:
        if self._ref_path(name).exists():
            raise ValueError(f"branch '{name}' already exists")
        current_commit = self.get_head_commit_hash()
        self._write_ref(name, current_commit)
        self.head_file.write_text(f"ref: refs/heads/{name}\n", encoding="utf-8")
        print(f"Created and switched to branch '{name}'")
        return name

    def checkout(self, name: str) -> str:
        if not self._ref_path(name).exists():
            raise ValueError(f"branch '{name}' does not exist")
        self.head_file.write_text(f"ref: refs/heads/{name}\n", encoding="utf-8")
        print(f"Switched to branch '{name}'")
        return name

    def list_branches(self) -> list[str]:
        if not self.heads_dir.exists():
            return []
        return sorted(path.name for path in self.heads_dir.iterdir() if path.is_file())

    def status(self) -> str:
        branch = self.get_current_branch()
        index = self.load_index()
        staged_files = sorted(index.keys())
        untracked_files = []
        for path in self.path.rglob("*"):
            if self.git_dir in path.parents or path.is_dir():
                continue
            rel_path = path.relative_to(self.path).as_posix()
            if rel_path not in index:
                untracked_files.append(rel_path)
        lines = [f"On branch {branch}"]
        if staged_files:
            lines.append("Changes to be committed:")
            for path in staged_files:
                lines.append(f"  staged: {path}")
        else:
            lines.append("No files staged yet.")
        if untracked_files:
            lines.append("Untracked files:")
            for path in sorted(untracked_files):
                lines.append(f"  {path}")
        return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A simple git clone") 
    subparse = parser.add_subparsers(dest="command", help="Available commands")

    subparse.add_parser("init", help="Initialize a new repository")

    add_parse = subparse.add_parser("add", help="Add the file or directory to staging")
    add_parse.add_argument("path", nargs="+", help="Files or directories to add")

    commit_parser = subparse.add_parser("commit", help="Commit your changes")
    commit_parser.add_argument("-m", "--message", help="commit message", required=True)
    commit_parser.add_argument("author", nargs="?", help="author name and email")

    status_parser = subparse.add_parser("status", help="Show repository status")
    status_parser.add_argument(
        "--short", action="store_true", help="Show a short status"
    )

    branch_parser = subparse.add_parser("branch", help="Create or list branches")
    branch_parser.add_argument("name", nargs="?", help="Branch name")

    checkout_parser = subparse.add_parser("checkout", help="Switch branches")
    checkout_parser.add_argument("branch", help="Branch name")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    repo = repository("")
    try:
        if args.command == "init":
            repo.init()
        elif args.command == "add":
            if not repo.git_dir.exists():
                print("not a git repository")
                return
            for path in args.path:
                repo.add_path(path)
        elif args.command == "commit":
            if not repo.git_dir.exists():
                print("not a git repository")
                return
            author = args.author or "pygit user <user@pygit.com>"
            repo.commit(args.message, author)
        elif args.command == "status":
            if not repo.git_dir.exists():
                print("not a git repository")
                return
            print(repo.status())
        elif args.command == "branch":
            if not repo.git_dir.exists():
                print("not a git repository")
                return
            if args.name:
                repo.branch(args.name)
            else:
                branches = repo.list_branches()
                print("Branches:")
                for branch in branches:
                    print(f"  {branch}")
        elif args.command == "checkout":
            if not repo.git_dir.exists():
                print("not a git repository")
                return
            repo.checkout(args.branch)
    except Exception as exc:
        print(f"error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
