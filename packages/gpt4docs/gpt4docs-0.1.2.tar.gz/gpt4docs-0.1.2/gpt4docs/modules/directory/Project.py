from pathlib import Path
from gpt4docs.modules.directory import File
import logging

logger = logging.getLogger(__name__)


class Project:
    def __init__(self, project_root: str | Path):
        if isinstance(project_root, str):
            project_root = Path(project_root)

        self.project_root = project_root
        self.files = {
            self.get_file_path_by_path(file_path): File(file_path)
            for file_path in self.project_root.glob("**/*.py")
        }

    def save(self, suffix: str = "_commented", overwrite: bool = False):
        """Save the project to a new folder."""
        if overwrite:
            new_root = self.project_root
        else:
            new_root = self.project_root.parent / (self.project_root.name + suffix)

        for file in self.files.values():
            if not overwrite:
                # Replace name of the project root with the new root name
                dir_ = new_root / file.file_path.relative_to(self.project_root)
                dir_.parent.mkdir(parents=True, exist_ok=True)
                logger.debug(f"Saving {file.file_path} to {dir_}")
                file.save(dir_, overwrite=False)
            else:
                logger.debug(f"Overwrites {file.file_path}")
                file.save(overwrite=True)

        logger.info(f"Saved {len(self.files)} files to {new_root}")
        return new_root

    def _tree(self, dir_path: Path, padding: str = "", print_files: bool = True):
        """Represent the directory tree as a string."""
        # Tree based on https://stackoverflow.com/a/9728478/4416928
        if dir_path.is_dir():
            dirs = [d for d in dir_path.iterdir() if d.is_dir()]
            files = [f for f in dir_path.iterdir() if f.is_file()]
            if not dirs and not files:
                return f"{padding}└── {dir_path.name}/"
            if print_files:
                contents = [
                    *map(lambda d: self._tree(d, padding + "│   "), dirs),
                    *map(lambda f: f"{padding}│   ├── {f.name}", files),
                ]
            else:
                contents = [*map(lambda d: self._tree(d, padding + "│   "), dirs)]
            return "\n".join(
                [f"{padding}├── {dir_path.name}/", *contents, f"{padding}└──"]
            )
        else:
            return f"{padding}└── {dir_path.name}"

    def get_file_path_by_path(self, file_path: str) -> str:
        """Get the file path relative to the project root."""
        return str(file_path.relative_to(self.project_root))

    def get_file_path(self, file: File) -> str:
        """Get the file path relative to the project root."""
        return self.get_file_path_by_path(file.file_path)

    def get_file(self, file: File) -> File:
        return self.files[self.get_file_path(file)]

    def __str__(self) -> str:
        return self._tree(self.project_root, print_files=True)
