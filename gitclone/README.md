# pygit Clone Project

## Project Overview

This project implements a small Python-based Git-like repository manager called `pygit`.
It supports initializing a new repository and adding files or directories to a simple object database stored under `.pygit`.

## Features

- Initialize a new repository structure with `.pygit`, `.pygit/objects`, and `.pygit/refs`
- Create a HEAD file that points to the default branch `refs/heads/master`
- Save a repository index in JSON format for staging files
- Add individual files or all files inside a directory to staging
- Compute SHA-1 hashes for stored objects, matching Git-style hashing behavior
- Compress object data with `zlib` and store it in a content-addressed object database

## How It Works

1. `init`: Creates the `.pygit` directory structure and writes metadata files.
2. `add`: Reads file bytes, creates a `Blob` object, serializes and compresses the content, and stores it under `.pygit/objects`.
3. The index file keeps a mapping from file path to object hash for staged content.

## Command Usage

- `python main.py init`
  - Initializes a new `pygit` repository in the current folder.
- `python main.py add <path>...`
  - Adds one or more files or directories to the repository staging index.
  - Example: `python main.py add README.md src/`

## Code Structure

- `Gitobject` class
  - Represents a generic Git object with `type` and `content`.
  - Methods:
    - `hash()`: Computes the SHA-1 hash of the object header and content.
    - `serialize()`: Compresses object data using `zlib`.
    - `deserialize()`: Decompresses serialized data and recreates the object instance.
- `Blob` class
  - Subclass of `Gitobject` for storing raw file contents.
  - Automatically sets object type to `blob`.
- `repository` class
  - Manages repository paths and storage behavior.
  - Methods:
    - `init()`: Creates repository folders and index files.
    - `load_index()`: Loads the staging index from `.pygit/index`.
    - `store_object()`: Saves serialized objects into `.pygit/objects`.
    - `save_index()`: Writes the index JSON file.
    - `add_file()`: Adds a single file to the index.
    - `add_dir()`: Recursively adds files from a directory.
    - `add_path()`: Adds either a file or directory path.
- `main()` function
  - Parses command-line arguments via `argparse`.
  - Dispatches `init` and `add` commands.

## Libraries Used

- `argparse`
  - Used to parse command-line arguments and options.
- `sys`
  - Used to exit the program with an error status on exception.
- `pathlib.Path`
  - Used for file and directory path handling in a cross-platform way.
- `json`
  - Used for reading and writing the staging index in JSON format.
- `hashlib`
  - Used to compute a SHA-1 hash for object identity.
- `zlib`
  - Used to compress and decompress object content.

## Important Parameters and Keywords

- `path`: The file or directory path provided to the `add` command.
- `.pygit`: The hidden repository storage folder, analogous to Git's `.git` folder.
- `HEAD`: A file that points to the current branch reference.
- `refs/heads/master`: The default branch reference path stored in `HEAD`.
- `objects`: The folder where object files are stored using the first two characters of their SHA-1 hash as a directory.
- `index`: A JSON file that tracks staged files mapped to object hashes.

## Special Notes

- The repository only supports basic object storage and staging; it does not implement commits, branches, or history traversal.
- When adding directories, `add_dir()` skips files inside the `.pygit` directory to avoid indexing repository internals.
- The implementation uses the same object header format as Git: `<type> <size>\0<content>`.

## Project Goals

- Demonstrate fundamental Git internals in Python.
- Provide a simple example of content-addressed storage.
- Show using file hashing and compression for object persistence.
- Keep the implementation readable and easy to extend.
