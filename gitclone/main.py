# global class can access to easyly for help of current location can be access .
from __future__ import annotations
import argparse
import json
import logging
import sys
from pathlib import Path
import zlib

logging.getLogger().setLevel(logging.CRITICAL)

import hashlib


class Gitobject:
    def __init__(self, obj_type: str, content: bytes):
        self.type = obj_type
        self.content = content

    # hash libary - to check the file can be change or not .
    # encode - to convert string to byte .
    # hexdigest - hash object can be read it and convert into hexdecimal
    def hash(self) -> str:
        header = f"{self.type} {len(self.content)}\0".encode()
        return hashlib.sha1(header + self.content).hexdigest()

    # zlib - it is python build libary which are used to compress and decompress of the data
    # compress - large data convert into small data .
    # decompress - small data convert into orginal data
    def serialize(self) -> bytes:
        header = f"{self.type} {len(self.content)}\0".encode()
        return zlib.compress(header + self.content)

    @classmethod

    # decode - it is mainly used to convert the data encode in proper format for readbility .
    def deserialize(cls, data: bytes) -> Gitobject:
        decompress = zlib.decompress(data)
        null_id = decompress.find(b"\0")
        header = decompress[:null_id]
        content = decompress[null_id + 1 :]

        obj_type, _ = header.split(b" ", 1)

        return cls(obj_type.decode(), content)


class Blob(Gitobject):
    # super()- it is python built function which are used to allow the proxy object to call themselves .

    def __init__(self, content: bytes):
        super().__init__("blob", content)

    def get_container(self) -> bytes:
        return self.content


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


# resolve() path ko absolute path me convert karta hai
# absolute path means full path from root folder
# __init__- is constructor which are used to the run a fuction with automatically .
class repository:
    def __init__(self, path):
        self.path = Path(path).resolve()

        # .pygit folder
        self.git_dir = self.path / ".pygit"

        # .pygit/objects folder
        self.object_dir = self.git_dir / "objects"

        # .pygit/refs folder
        self.ref_dir = self.git_dir / "refs"

        # .pygit/HEAD file
        self.head_file = self.git_dir / "HEAD"

        # .pygit/index file
        self.index_file = self.git_dir / "index"

    def init(self):
        # folders create
        self.git_dir.mkdir(exist_ok=True)
        self.object_dir.mkdir(exist_ok=True)
        self.ref_dir.mkdir(exist_ok=True)

        # HEAD file create and write
        self.head_file.write_text("ref: refs/heads/main\n")

        self.save_index({})

        # dump-Json data can be  direct written in file .
        # dumps- Json data can convert into string form .
        # index file create
        self.index_file.write_text(json.dumps({}, indent=4))

        print(f"Initialized empty pygit repository in {self.git_dir}")
        return True

    def load_index(self) -> dict[str, str]:
        if not self.index_file.exists():
            return {}

        try:
            return json.loads(self.index_file.read_text())
        except:
            return {}

    def store_object(self, obj: Gitobject):
        obj_hash = obj.hash()
        object_dir = self.object_dir / obj_hash[:2]
        object_file = object_dir / obj_hash[2:]

        if not object_file.exists():
            object_dir.mkdir(exist_ok=True)
            object_file.write_bytes(obj.serialize())

        return obj_hash

    def save_index(self, index: dict[str, str]):
        self.index_file.write_text(json.dumps(index, indent=2))

    def add_file(self, path: str):
        full_path = self.path / path

        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found ")

            # read the file content
        content = full_path.read_bytes()

        # create blob object from content .
        blob = Blob(content)

        # store the blob object in database    (.git/objects) .
        blob_hash = self.store_object(blob)

        index = self.load_index()
        index[path] = blob_hash
        self.save_index(index)
        pass

        print(f"Added {path}")

    def add_dir(self, path: str):

        full_path = self.path / path

        for file_path in full_path.rglob("*"):

            if self.git_dir in file_path.parents:
                continue
            # as_posix- it is used to create the folder in subfolder to exists now . (folder-subfolder).
            if file_path.is_file():
                rel_path = file_path.relative_to(self.path).as_posix()
                self.add_file(rel_path)

    def add_path(self, path: str) -> None:
        full_path = self.path / path

        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found ")

        if full_path.is_file():
            self.add_file(path)
        elif full_path.is_dir():
            self.add_dir(path)
        else:
            raise ValueError(f"{path} is found in file and folder ")

    def create_tree_from_index(self):
        index = self.load_index()
        tree_entries = {}

        for path, blob_hash in sorted(index.items()):
            current = tree_entries
            parts = path.split("/")
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = blob_hash

        def build_tree(node):
            tree = Tree([])
            for name in sorted(node):
                value = node[name]
                if isinstance(value, dict):
                    obj_hash = build_tree(value)
                    tree.add_entries(name, "40000", obj_hash)
                else:
                    tree.add_entries(name, "100644", value)
            return self.store_object(tree)

        return build_tree(tree_entries)

    def commit(self, message: str, author: str = "PyGituser <user@pygit.com>"):
        hash_tree = self.create_tree_from_index()
        print(f"Created tree {hash_tree}")


def main():
    parser = argparse.ArgumentParser(description="A simple git clone")

    subparse = parser.add_subparsers(dest="command", help="Available commands")
    # init command
    init_parse = subparse.add_parser("init", help="Initialize a new repository")

    # add command - to add file and store in staging to them.
    add_parse = subparse.add_parser("add", help="Add the file and directory to staging")
    add_parse.add_argument("path", nargs="+", help="Files or directories to add")

    # commit commands .
    commit_parser = subparse.add_parser("commit", help="commit your message ")
    commit_parser.add_argument("-m", "--message", help="commit message", required=True)
    commit_parser.add_argument("author", help="author name and email")

    args = parser.parse_args()

    print(args)

    if not args.command:
        parser.print_help()
        return

    repo = repository("")
    try:
        if args.command == "init":
            repo.init()
            return
        elif args.command == "add":
            if not repo.git_dir.exists():
                print("not repositor can be present ")
                return

            for path in args.path:
                repo.add_path(path)

        elif args.command == "commit":
            if not repo.git_dir.exists():
                print("not  a git repositor  ")
                return
            author = args.author or "pygit user <user@pygit.com>"
            repo.commit(args.message, author)

    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)


main()
