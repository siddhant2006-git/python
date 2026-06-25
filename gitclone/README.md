# PyGit (simple git-like toy)

This small project is an educational implementation of the core ideas behind `git`, written in Python. It is intended as a toy repository manager that demonstrates how Git-style object storage, indexing, and simple command handling works.

## Project overview

- **Purpose:** learn how Git stores objects and tracks files by implementing a minimal version of `git init`, `git add`, and `git commit`.
- **Language:** Python 3.9+
- **Main file:** `main.py`
- **Repository folder:** `gitclone`

## What this project implements

- A `.pygit` repository directory with basic metadata files.
- SHA-1 based object hashing for file data and tree structures.
- A simple index file that maps working tree paths to object hashes.
- File and directory staging support via `add`.
- A command-line interface with subcommands.

## Files and structure

- `gitclone/main.py`
  - Full implementation of the toy Git engine.
  - Contains the core classes `Gitobject`, `Blob`, `Tree`, and `repository`.
- `gitclone/README.md`
  - Project documentation and usage notes.
- `.pygit/`
  - Local repository metadata created by `python main.py init`.

## Key concepts in the code

### Gitobject

`Gitobject` is the base class for every stored object. It provides:

- `hash()`: computes the object SHA-1 based on the Git header format `"{type} {len(content)}\0" + content`.
- `serialize()`: compresses the object bytes with `zlib` for storage.
- `deserialize()`: decompresses bytes, splits the header and body, then returns a new `Gitobject`.

### Blob

`Blob` is a simple subclass of `Gitobject` for file data. It stores raw file bytes and can be written to the object database.

### Tree

`Tree` is designed to represent directory contents. Each entry is stored as a tuple of:

- `name` — file or directory name
- `mode` — object mode string like `100644` for files or `40000` for directories
- `obj_hash` — object hash of the child blob or subtree

The tree serializes entries into the Git-style format: `mode name\0` followed by raw hash bytes.

### Repository

The `repository` class manages the working directory and repository metadata:

- `init()`: creates `.pygit`, object and ref directories, `HEAD`, and an empty `index` file.
- `load_index()`: reads `.pygit/index` and returns the tracked path->hash mapping.
- `store_object()`: saves compressed object bytes under `.pygit/objects/<first2>/<rest>`.
- `save_index()`: writes the index JSON file.
- `add_file()`: stores a file as a blob and updates the index.
- `add_dir()`: walks a directory recursively and stages every file under it.
- `add_path()`: chooses between file and directory staging.
- `create_tree_from_index()`: builds tree objects from the current index.
- `commit()`: starts creating a commit from the current index.

## How to use

1. Install Python 3.9 or later.
2. Open a terminal inside `python/gitclone`.
3. Run commands:

```bash
python main.py init
python main.py add README.md
python main.py add folder_name
python main.py commit -m "Initial commit" "Your Name <you@example.com>"
```

Use `python main.py` with no arguments to display the help text.

## Example workflow

```bash
python main.py init
python main.py add sample.txt
python main.py add src/
python main.py commit -m "Add project files" "Developer <dev@example.com>"
```

## Current limitations and next steps

This project is a learning prototype, not a full Git implementation. Some current limitations include:

- `commit()` is not yet fully implemented: it creates a tree object but does not currently write commit metadata or update refs.
- Tree parsing and object deserialization are still under refinement.
- The implementation assumes a simple file mode and does not support symbolic links, executable bits, or merge history.
- Error handling is minimal and mostly focused on the happy path.

## Notes for developers

- The code lives entirely in `gitclone/main.py`.
- The repository metadata is stored in `.pygit`, not `.git`.
- The index file is JSON and can be viewed directly.
- The object database uses SHA-1 hashes and zlib compression, similar to Git.

## Want help improving this project?

I can help with the following additional improvements:

- finish `commit()` so it writes actual commit objects and updates `.pygit/HEAD`
- make the tree logic fully recursive for nested directories
- add tests for `init`, `add`, and `commit`
- document the object storage format in more detail
