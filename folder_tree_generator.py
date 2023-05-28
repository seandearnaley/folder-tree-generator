"""Generate a text representation of a folder."""
import argparse
from pathlib import Path
from typing import List, Optional


def _parse_ignore_patterns(ignorefile_path: Path) -> List[str]:
    """Parse a .gitignore like ignore file and return a list of ignored patterns."""
    with open(ignorefile_path, encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]


def _is_ignored(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a file or folder should be ignored."""
    return entry.name == ".gitignore" or any(
        entry.match(pattern) for pattern in ignored_patterns
    )


def _list_entries(root: Path) -> List[Path]:
    """List entries in a directory, sorted by type and name."""
    return sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))


def _entry_to_string(entry: Path, indent: str, ignored_patterns: List[str]) -> str:
    """Convert a file system entry to its string representation."""
    if (
        entry.is_dir()
        and not _is_ignored(entry, ignored_patterns)
        and entry.name != ".git"
    ):
        subtree = _generate_folder_tree(entry, indent + "|   ", ignored_patterns)
        return f"{indent}|-- {entry.name}/\n{subtree}"
    if entry.is_file() and not _is_ignored(entry, ignored_patterns):
        return f"{indent}|-- {entry.name}\n"

    return ""


def _generate_folder_tree(
    root: Path, indent: str = "", ignored_patterns: Optional[List[str]] = None
) -> str:
    """Generate a tree of a folder."""
    if ignored_patterns is None:
        ignored_patterns = []

    entries = _list_entries(root)
    tree_str = "".join(
        _entry_to_string(entry, indent, ignored_patterns) for entry in entries
    )

    return tree_str


def _parse_arguments() -> str:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a text representation of a folder."
    )
    parser.add_argument("root_folder", type=str, help="Path to the root folder")

    args = parser.parse_args()

    root_folder: str = args.root_folder

    # Check if the root folder exists and is a directory
    if not Path(root_folder).is_dir():
        raise ValueError(f"{root_folder} is not a valid directory")

    return root_folder


def generate_tree(root_folder: str, ignore_file_name: Optional[str] = None) -> str:
    """Generate a tree of a folder."""
    root = Path(root_folder)
    ignorefile_path = root / ignore_file_name if ignore_file_name else None
    ignored_patterns = (
        _parse_ignore_patterns(ignorefile_path)
        if ignorefile_path and ignorefile_path.exists()
        else []
    )

    tree_str = f"{root.name}/\n"
    tree_str += _generate_folder_tree(root, ignored_patterns=ignored_patterns)
    return tree_str


def _main() -> None:
    """Main function."""
    root_folder = _parse_arguments()
    output_text = generate_tree(root_folder, ignore_file_name=".gitignore")
    print(output_text)


if __name__ == "__main__":
    _main()
