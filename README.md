# Folder Tree Generator

This script generates a tree representation of a folder's structure, including subfolders and files. It also takes into account `.gitignore` files to exclude ignored files and folders from the generated tree.

## Why?

I needed a way to generate folder structures in a standard text format that I could copy and paste into GPT without including all the build artifacts, eg. repository structures for code analysis.  If you wanted to make your own ignore file it should be a simple adapation of a gitignore file, in 90% of my use cases, the gitignore is sufficient.

## Usage

To use the script, run the following command:

```bash
python3 main.py <root_folder>
```

Replace `<root_folder>` with the path to the folder you want to generate the tree for.

## Example

Suppose you have the following folder structure:

```
my_project/
|-- .gitignore
|-- main.py
|-- utils.py
|-- data/
|   |-- input.txt
|   |-- output.txt
```

And the `.gitignore` file contains:

```
data/output.txt
```

Running the script with `python3 main.py my_project` will output the following tree:

```
my_project/
|-- .gitignore
|-- main.py
|-- utils.py
|-- data/
|   |-- input.txt
```

As you can see, the `data/output.txt` file is excluded from the tree because it's listed in the `.gitignore` file.

## Functions

The script contains the following functions:

- `parse_gitignore(gitignore_path: Path) -> List[str]`: Parses a `.gitignore` file and returns a list of ignored patterns.
- `should_ignore(entry: Path, ignored_patterns: List[str]) -> bool`: Checks if a file or folder should be ignored based on the list of ignored patterns.
- `generate_tree(root: Path, indent: str = "", ignored_patterns: Optional[List[str]] = None) -> str`: Generates a tree of a folder, taking into account the ignored patterns.
- `main(root_folder: str) -> None`: The main function that takes the root folder as an argument and prints the generated tree.

## Requirements

- Python 3.6 or higher
- The `pathlib` library (included in the Python standard library since version 3.4)
