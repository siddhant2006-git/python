# global class can access to easyly for help of current location can be access .
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import json
import hashlib
import zlib

class Gitobject:
    def __init__(self,obj_type:str,content:bytes):
        self.type=obj_type
        self.content=content

    # hash libary - to check the file can be change or not .
    # encode - to convert string to byte .
    # hexdigest - hash object can be read it and convert into hexdecimal
    def hash(self) -> str :
        header=f"{self.type} {len(self.content)}\0".encode()
        return hashlib.sha1(header +self.content).hexdigest()

    # zlib - it is python build libary which are used to compress and decompress of the data
    # compress - large data convert into small data .
    # decompress - small data convert into orginal data
    def serialize(self) -> bytes:
        header = f"{self.type} {len(self.content)}\0".encode()
        return zlib.compress(header +self.content)
    @classmethod

    def deserialize(cls,data:bytes) -> Gitobject:
        decompress=zlib.decompress(data)
        null_id=decompress.find(b"\0")
        header=decompress[:null_id]
        content=decompress[null_id +1:]

        obj_type ,_ =header.split(b" ",1)


        return cls(obj_type.decode(),content)

class Blob(Gitobject):
    
    def __init__(self, content:bytes):
        super().__init__("blob", content)

    def get_container(self) ->bytes:
          return   self.content


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

        self.save_index({})

        # dump-Json data can be  direct written in file .
        # dumps- Json data can convert into string form .
        # index file create
        self.index_file.write_text(json.dumps({}, indent=4))

        print(f"Initialized empty pygit repository in {self.git_dir}")
        return True

    def load_index(self) ->dict[str,str]:
        if not self.index_file.exists():
            return {}

        try:
            return json.loads(self.index_file.read_text())
        except:
            return {}

    def store_object(self,obj:Gitobject):
        obj_hash=obj.hash()
        object_dir=self.object_dir /obj_hash[:2]
        object_file=object_dir /obj_hash[2:]

        if not object_file.exists():
            object_dir.mkdir(exist_ok=True)
            object_file.write_bytes(obj.serialize())

        return obj_hash

    def save_index(self,index:dict[str,str]):
        self.index_file.write_text(json.dumps(index,indent=2))

    def add_file(self ,path:str):
        full_path=self.path /path

        if not full_path.exists():
            raise FileNotFoundError(f"Path {path} is not found ")

            # read the file content
        content=full_path.read_bytes()

        # create blob object from content .
        blob=Blob(content)

        # store the blob object in database    (.git/objects) .
        blob_hash=self.store_object(blob)

        index=self.load_index()
        index[path]=blob_hash
        self.save_index(index)
        pass

        print(f"Added {path}")

    def add_dir(self, path: str):
        
     full_path = self.path / path

     for file_path in full_path.rglob("*"):

        if self.git_dir in file_path.parents:
            continue

        if file_path.is_file():
            rel_path = file_path.relative_to(self.path).as_posix()
            self.add_file(rel_path)

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

            for path in args.path:
                repo.add_path(path)
            

    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)


main()
