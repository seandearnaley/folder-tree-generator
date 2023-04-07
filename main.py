"""Generate a tree of a folder."""
from pathlib import Path
from typing import List, Optional


def parse_gitignore(gitignore_path: Path) -> List[str]:
    """Parse a .gitignore file and return a list of ignored patterns."""
    ignored_patterns: List[str] = []
    with open(gitignore_path, encoding="utf-8") as file:
        for line in file:
            pattern = line.strip()
            if not pattern or pattern.startswith("#"):
                continue
            ignored_patterns.append(pattern)
    return ignored_patterns


def should_ignore(entry: Path, ignored_patterns: List[str]) -> bool:
    """Check if a file or folder should be ignored."""
    for pattern in ignored_patterns:
        if entry.match(pattern):
            return True
    return False


def generate_tree(
    root: Path,
    indent: str = "",
    ignored_patterns: Optional[List[str]] = None,
) -> str:
    """Generate a tree of a folder."""
    tree_str = ""

    if ignored_patterns is None:
        ignored_patterns = []

    entries = sorted(root.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    for entry in entries:
        if should_ignore(entry, ignored_patterns):
            continue

        if entry.is_dir():
            if entry.name == ".git":
                continue

            if entry.name == ".gitignore":
                ignored_patterns.extend(parse_gitignore(entry))

            tree_str += f"{indent}|-- {entry.name}/\n"
            tree_str += generate_tree(entry, indent + "|   ", ignored_patterns)
        else:
            tree_str += f"{indent}|-- {entry.name}\n"

    return tree_str


def main(root_folder: str) -> None:
    """Main function."""
    root = Path(root_folder)
    gitignore_path = root / ".gitignore"
    ignored_patterns = (
        parse_gitignore(gitignore_path) if gitignore_path.exists() else []
    )

    tree_str = f"{root.name}/\n"
    tree_str += generate_tree(root, ignored_patterns=ignored_patterns)
    print(tree_str)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <root_folder>")
        sys.exit(1)

    main(sys.argv[1])
