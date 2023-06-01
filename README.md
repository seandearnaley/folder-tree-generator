# Folder Tree Generator


[![PyPI version](https://badge.fury.io/py/folder-tree-generator.svg)](https://badge.fury.io/py/folder-tree-generator)

![Test](https://github.com/seandearnaley/folder-tree-generator/workflows/Run%20pytest/badge.svg)


Folder Tree Generator is a Python module that takes a folder path and outputs a text representation of the folders and files. It supports ignore files, such as `.gitignore`, to exclude certain files or folders from the output.

typical string output:

```text
my_project/
|-- .gitignore
|-- main.py
|-- utils.py
|-- data/
|   |-- input.txt
|   |-- output.txt
```

## Why?

I needed a way to generate folder structures in a standard text format that I could copy and paste into GPT without including all the build artifacts, eg. repository structures for code analysis.  If you wanted to make your own ignore file it should be a simple adapation of a gitignore file, in 90% of my use cases, the gitignore is sufficient.

## Installation

You can install the module from PyPI using pip:

```bash
pip install folder-tree-generator
```

## Usage

You can use the module as a command-line tool or import it in your Python script.

### Command-line usage

```bash
python -m folder_tree_generator/folder_tree_generator /path/to/your/folder
```

### Python script usage

```python
from folder_tree_generator import generate_tree

output_text = generate_tree("/path/to/your/folder")
print(output_text)
```

## Configuration

By default, the module looks for a `.gitignore` file in the root folder to determine which files and folders to ignore. You can change the ignore file name by passing an optional argument to the `generate_tree` function:

```python
output_text = generate_tree("/path/to/your/folder", ignore_file_name=".myignore")
```

## Development

To set up the development environment, clone the repository and install the required dependencies using Poetry:

```bash
git clone https://github.com/seandearnaley/folder-tree-generator.git
cd folder-tree-generator
poetry install
```

To run the tests, use the following command:

```bash
poetry run pytest
```

Make sure to update the README.md file with these changes.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/seandearnaley/folder-tree-generator).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.