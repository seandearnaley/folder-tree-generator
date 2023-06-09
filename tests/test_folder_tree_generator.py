"""Tests for folder_tree_generator."""
import argparse
import sys
from pathlib import Path
from typing import Union

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture

from folder_tree_generator.folder_tree_generator import (
    entry_to_string,
    expand_user_path,
    generate_folder_tree,
    generate_tree,
    is_ignored,
    list_entries,
    main,
    parse_arguments,
    parse_ignore_patterns,
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
    patterns = parse_ignore_patterns(sample_ignore_file)
    assert patterns == ["*.txt", "*.log"]


def test_is_ignored(sample_directory: Path) -> None:
    """Test if a file or folder should be ignored."""
    ignored_patterns = ["*.txt", "*.log"]
    assert is_ignored(sample_directory / "file1.txt", ignored_patterns)
    assert is_ignored(sample_directory / "file2.log", ignored_patterns)
    assert not is_ignored(sample_directory / "folder1", ignored_patterns)


def test_list_entries(sample_directory: Path) -> None:
    """Test listing of entries in a directory."""
    entries = list_entries(sample_directory)
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
        entry_to_string(sample_directory / "folder1", "", ignored_patterns)
        == "|-- folder1/\n"
    )
    assert entry_to_string(sample_directory / "file1.txt", "", ignored_patterns) == ""


def test_generate_folder_tree(sample_directory: Path) -> None:
    """Test generation of a tree of a folder."""
    ignored_patterns = ["*.txt", "*.log"]
    tree_str = generate_folder_tree(sample_directory, ignored_patterns=ignored_patterns)
    assert tree_str == "|-- folder1/\n|-- folder2/\n"


def test_generate_folder_tree_with_ignore(sample_directory: Path) -> None:
    """Test generation of a tree of a folder."""
    tree_str = generate_folder_tree(sample_directory, ignored_patterns=None)
    assert tree_str == "|-- folder1/\n|-- folder2/\n|-- file1.txt\n|-- file2.log\n"


def test_generate_tree(sample_directory: Path, sample_ignore_file: Path) -> None:
    """Test main function."""
    tree_str = generate_tree(
        str(sample_directory), ignore_file_path=str(sample_ignore_file)
    )
    expected_tree_str = f"{sample_directory.name}/\n|-- folder1/\n|-- folder2/\n"
    assert tree_str == expected_tree_str


def test_main(
    sample_directory: Path, sample_ignore_file: Path, capsys: CaptureFixture[str]
) -> None:
    """Test main function."""
    # Move the sample_ignore_file to the sample_directory
    sample_ignore_file.rename(sample_directory / sample_ignore_file.name)

    # Call main with sample_directory
    sys.argv = [
        "folder_tree_generator.py",
        str(sample_directory),
        "--ignore_file_path",
        str(sample_ignore_file),
    ]
    main()

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
    ignored_patterns: list[str],
    expected_result: Union[bool, str],
) -> None:
    """Test handling of different entries."""
    if entry_name == ".git":
        (sample_directory / entry_name).mkdir()
    else:
        (sample_directory / entry_name).write_text("content")

    entry = sample_directory / entry_name

    if isinstance(expected_result, bool):
        assert is_ignored(entry, ignored_patterns) == expected_result
    else:
        assert entry_to_string(entry, "", ignored_patterns) == expected_result


def test_parse_arguments(mocker: MockerFixture) -> None:
    """Test parsing of command line arguments."""

    mocker.patch("sys.argv", ["script.py", "root_folder"])
    assert parse_arguments() == argparse.Namespace(
        root_folder="root_folder", report_file_path="report.txt", ignore_file_path=None
    )


def test_generate_tree_invalid_root_folder() -> None:
    """Test generate_tree function with an invalid root folder."""
    with pytest.raises(ValueError) as excinfo:
        generate_tree("invalid_folder")
    assert str(excinfo.value) == "invalid_folder is not a valid directory"


def test_generate_tree_invalid_ignore_file_path(sample_directory: Path) -> None:
    """Test generate_tree function with an invalid ignore file path."""
    with pytest.raises(ValueError) as excinfo:
        generate_tree(str(sample_directory), ignore_file_path="invalid_file")
    assert str(excinfo.value) == "invalid_file is not a valid file"


def test_expand_user_path():
    """Test expand_user_path function."""
    # test with a relative path
    relative_path = "test_dir/test_file"
    assert expand_user_path(relative_path) == relative_path

    # test with a home directory shortcut
    home_shortcut_path = "~/test_dir/test_file"
    expected_path = Path(home_shortcut_path).expanduser().resolve()
    assert expand_user_path(home_shortcut_path) == str(expected_path)

    # test with None
    assert expand_user_path(None) is None
