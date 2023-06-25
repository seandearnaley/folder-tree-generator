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

I needed a way to generate folder structures in a standard text format that I could copy and paste into GPT without including all the build artifacts, eg. repository structures for code analysis. If you wanted to make your own ignore file it should be a simple adapation of a gitignore file, in 90% of my use cases, the gitignore is sufficient.

## Installation

You can install the module from PyPI using pip:

```bash
pip install folder-tree-generator
```

or via Poetry:

```bash
poetry add folder-tree-generator
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

## Optional Parameters

- `--report_file_path`: The name of the report file. Defaults to `report.txt` if not provided.
- `--ignore_file_path`: The path to the ignore file. If provided, the script will parse the ignore patterns from the file and exclude the matching files and folders from the report.

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

## Checking Test Coverage

This project uses the `coverage` package to generate test coverage reports. Here's how to use it:

1. First, you need to install the `coverage` package if it's not already installed.

```bash
pip install coverage
```

or

```bash
poetry add coverage
```

If you're using Poetry, you can also add `coverage` to your `pyproject.toml` file and run `poetry install` to install it.

2. After installing `coverage`, you can use it to run your tests and collect coverage data. If you're using `pytest` for testing, you can use the following command:

```bash
coverage run -m pytest
```

This command tells `coverage` to run `pytest` as a module (hence the `-m` flag), and `coverage` collects data about which parts of your code were executed during the test run.

3. Once you've collected coverage data, you can generate a report by running:

```bash
coverage report
```

This will print a coverage report to the terminal, showing the code coverage for each module in your project.

4. If you want a more detailed view, you can generate an HTML report using:

```bash
coverage html
```

This will generate an `htmlcov` directory in your project directory. Inside this directory, you'll find an `index.html` file. You can open this file in a web browser to view a detailed coverage report that shows which lines of each file were covered by the tests.

5. If you're finished checking coverage and want to clear the collected data, you can use the command:

```bash
coverage erase
```

This will delete the `.coverage` data file, clearing the collected coverage data.

Remember that code coverage is a useful tool for finding untested parts of your code, but achieving 100% code coverage doesn't necessarily mean your testing is perfect. It's important to write meaningful tests and not just strive for high coverage percentages.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on the [GitHub repository](https://github.com/seandearnaley/folder-tree-generator).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
