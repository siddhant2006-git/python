import argparse
import sys
from pathlib import Path
import json


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
        self.head_file.write_text("ref: refs/heads/master\n")

        # dump-Json data can be  direct written in file .
        # dumps- Json data can convert into string form .
        # index file create
        self.index_file.write_text(json.dumps({}, indent=4))

        print(f"Initialized empty pygit repository in {self.git_dir}")

        def add_path(self,path:str) ->None:
            full_path = self.path /path

            if not full_path.exists():
                raise FileNotFoundError(f"Path {path} is not found ")
            
            if full_path.is_file():
                self.add_file(path)
            elif full_path.is_dir():
                self.add_dir(path)
            else:
                raise ValueError(f"{path} is found in file and folder ")
            


def main():
    parser = argparse.ArgumentParser(description="A simple git clone")

    subparse = parser.add_subparsers(dest="command",help="Available commands")
    # init command
    init_parse = subparse.add_parser("init", help="Initialize a new repository")

    # add command - to add file and store in staging to them.
    add_parse = subparse.add_parser("add", help="Add the file and directory to staging")
    add_parse.add_argument("path", nargs="+", help="Files or directories to add")

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
        elif args.command =="add":
            if not repo.git_dir.exists():
                print("not repositor can be present ")
                return

            for path in args.paths:
                repo.add_path()
            

    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)


main()
