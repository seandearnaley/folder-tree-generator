"""Tests for folder_tree_generator."""
import sys
from pathlib import Path
from typing import Union

import pytest

from folder_tree_generator.folder_tree_generator import (
    _entry_to_string,
    _generate_folder_tree,
    _is_ignored,
    _list_entries,
    _main,
    _parse_arguments,
    _parse_ignore_patterns,
    generate_tree,
)


@pytest.fixture(name="sample_ignore_file")
def fixture_sample_ignore_file(tmp_path: Path) -> Path:
    """Create a sample .gitignore file."""
    content = "*.txt\n*.log\n# This is a comment\n"
    ignore_file_path = tmp_path / ".gitignore"
    ignore_file_path.write_text(content)
    return ignore_file_path


@pytest.fixture(name="sample_directory")
def fixture_sample_directory(tmp_path: Path) -> Path:
    """Create a sample directory."""
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder2").mkdir()
    (tmp_path / "file1.txt").write_text("file1 content")
    (tmp_path / "file2.log").write_text("file2 content")
    return tmp_path


def test_parse_ignore_patterns(sample_ignore_file: Path) -> None:
    """Test parsing of .gitignore file."""
    patterns = _parse_ignore_patterns(sample_ignore_file)
    assert patterns == ["*.txt", "*.log"]


def test_is_ignored(sample_directory: Path) -> None:
    """Test if a file or folder should be ignored."""
    ignored_patterns = ["*.txt", "*.log"]
    assert _is_ignored(sample_directory / "file1.txt", ignored_patterns)
    assert _is_ignored(sample_directory / "file2.log", ignored_patterns)
    assert not _is_ignored(sample_directory / "folder1", ignored_patterns)


def test_list_entries(sample_directory: Path) -> None:
    """Test listing of entries in a directory."""
    entries = _list_entries(sample_directory)
    assert entries == [
        sample_directory / "folder1",
        sample_directory / "folder2",
        sample_directory / "file1.txt",
        sample_directory / "file2.log",
    ]


def test_entry_to_string(sample_directory: Path) -> None:
    """Test conversion of a directory entry to its string representation."""
    ignored_patterns = ["*.txt", "*.log"]
    assert (
        _entry_to_string(sample_directory / "folder1", "", ignored_patterns)
        == "|-- folder1/\n"
    )
    assert _entry_to_string(sample_directory / "file1.txt", "", ignored_patterns) == ""


def test_generate_folder_tree(sample_directory: Path) -> None:
    """Test generation of a tree of a folder."""
    ignored_patterns = ["*.txt", "*.log"]
    tree_str = _generate_folder_tree(
        sample_directory, ignored_patterns=ignored_patterns
    )
    assert tree_str == "|-- folder1/\n|-- folder2/\n"


def test_generate_folder_tree_with_ignore(sample_directory: Path) -> None:
    """Test generation of a tree of a folder."""
    tree_str = _generate_folder_tree(sample_directory, ignored_patterns=None)
    assert tree_str == "|-- folder1/\n|-- folder2/\n|-- file1.txt\n|-- file2.log\n"


def test_generate_tree(sample_directory: Path, sample_ignore_file: Path) -> None:
    """Test main function."""
    # Move the sample_ignore_file to the sample_directory
    sample_ignore_file.rename(sample_directory / sample_ignore_file.name)
    tree_str = generate_tree(
        str(sample_directory), ignore_file_name=sample_ignore_file.name
    )
    expected_tree_str = f"{sample_directory.name}/\n|-- folder1/\n|-- folder2/\n"
    assert tree_str == expected_tree_str


def test_main(sample_directory: Path, sample_ignore_file: Path, capsys) -> None:
    """Test main function."""
    # Move the sample_ignore_file to the sample_directory
    sample_ignore_file.rename(sample_directory / sample_ignore_file.name)

    # Call main with sample_directory
    sys.argv = ["folder_tree_generator.py", str(sample_directory)]
    _main()

    # Capture the output
    output = capsys.readouterr().out

    # Check the output
    expected_tree_str = f"{sample_directory.name}/\n|-- folder1/\n|-- folder2/\n\n"
    assert output == expected_tree_str


@pytest.mark.parametrize(
    "entry_name, ignored_patterns, expected_result",
    [
        (".gitignore", ["*.txt", "*.log"], True),
        (".git", ["*.txt", "*.log"], ""),
        ("ignored.txt", ["*.txt", "*.log"], ""),
    ],
)
def test_entry_handling_cases(
    sample_directory: Path,
    entry_name: str,
    ignored_patterns: list,
    expected_result: Union[bool, str],
) -> None:
    """Test handling of different entries."""
    if entry_name == ".git":
        (sample_directory / entry_name).mkdir()
    else:
        (sample_directory / entry_name).write_text("content")

    entry = sample_directory / entry_name

    if isinstance(expected_result, bool):
        assert _is_ignored(entry, ignored_patterns) == expected_result
    else:
        assert _entry_to_string(entry, "", ignored_patterns) == expected_result


def test_parse_arguments(mocker) -> None:
    """Test parsing of command line arguments."""

    # Mock the pathlib.Path.is_dir method
    is_dir_mock = mocker.patch("pathlib.Path.is_dir")

    # Test when the correct number of arguments is provided and root_folder is valid
    mocker.patch("sys.argv", ["script.py", "root_folder"])
    is_dir_mock.return_value = True
    assert _parse_arguments() == "root_folder"

    # Test when the provided root_folder is not a valid directory
    mocker.patch("sys.argv", ["script.py", "invalid_root_folder"])
    is_dir_mock.return_value = False
    with pytest.raises(ValueError) as exc_info:
        _parse_arguments()
    assert str(exc_info.value) == "invalid_root_folder is not a valid directory"
