"""Generate a text representation of a folder."""
import argparse
from pathlib import Path
from typing import List, Optional


def parse_ignore_patterns(ignorefile_path: Path) -> List[str]:
    """Parse a .gitignore like ignore file and return a list of ignored patterns."""
    with open(ignorefile_path, encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]


def is_ignored(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a file or folder should be ignored."""
    return entry.name == ".gitignore" or any(
        entry.match(pattern) for pattern in ignored_patterns
    )


def list_entries(root: Path) -> List[Path]:
    """List entries in a directory, sorted by type and name."""
    return sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))


def entry_to_string(entry: Path, indent: str, ignored_patterns: List[str]) -> str:
    """Convert a file system entry to its string representation."""
    if (
        entry.is_dir()
        and not is_ignored(entry, ignored_patterns)
        and entry.name != ".git"
    ):
        subtree = generate_folder_tree(entry, indent + "|   ", ignored_patterns)
        return f"{indent}|-- {entry.name}/\n{subtree}"
    if entry.is_file() and not is_ignored(entry, ignored_patterns):
        return f"{indent}|-- {entry.name}\n"

    return ""


def generate_folder_tree(
    root: Path, indent: str = "", ignored_patterns: Optional[List[str]] = None
) -> str:
    """Generate a tree of a folder."""
    if ignored_patterns is None:
        ignored_patterns = []

    entries = list_entries(root)
    tree_str = "".join(
        entry_to_string(entry, indent, ignored_patterns) for entry in entries
    )

    return tree_str


def generate_tree(root_folder: str, ignore_file_path: Optional[str] = None) -> str:
    """Generate a tree of a folder."""
    root = Path(root_folder)
    ignorefile_path = Path(ignore_file_path) if ignore_file_path else None

    if not root.is_dir():
        raise ValueError(f"{root_folder} is not a valid directory")

    if ignorefile_path is not None:
        if not ignorefile_path.is_file():
            raise ValueError(f"{ignore_file_path} is not a valid file")

    ignored_patterns = (
        parse_ignore_patterns(ignorefile_path)
        if ignorefile_path and ignorefile_path.exists()
        else []
    )

    tree_str = f"{root.name}/\n"
    tree_str += generate_folder_tree(root, ignored_patterns=ignored_patterns)
    return tree_str


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a text representation of a folder."
    )
    parser.add_argument("root_folder", type=str, help="Path to the root folder")
    parser.add_argument(
        "--report_file_path",
        type=str,
        default="report.txt",
        help="Name of the report file",
    )
    parser.add_argument(
        "--ignore_file_path",
        type=str,
        default=None,
        help="Path to the ignore file",
    )
    args = parser.parse_args()

    return args


def main() -> None:
    """Main function."""
    args = parse_arguments()
    root_folder = args.root_folder
    report_file_path = args.report_file_path
    ignore_file_path = args.ignore_file_path if args.ignore_file_path else None

    output_text = generate_tree(root_folder, ignore_file_path)

    with open(report_file_path, "w", encoding="utf-8") as file:
        file.write(output_text)

    print(output_text)


if __name__ == "__main__":
    main()
