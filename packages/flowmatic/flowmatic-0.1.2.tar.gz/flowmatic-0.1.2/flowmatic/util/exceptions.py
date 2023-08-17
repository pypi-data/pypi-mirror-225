"""Exceptions used by Appy.

Classes:
    SavedClassLoadException: Raised when a class cannot be loaded from a saved file."""


from typing import Any


class SavedClassLoadException(Exception):
    path: str

    def __init__(self, path: str) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"Could not load class from {self.path}"


class TooManyFilesError(Exception):
    max_files: int

    def __init__(self, max_files: int) -> None:
        self.max_files = max_files

    def __str__(self) -> str:
        return f"Too many files. Max: {self.max_files}"


class NotAFileError(Exception):
    path: Any

    def __init__(self, path: Any) -> None:
        self.path = path

    def __str__(self) -> str:
        return f"Not a file: {self.path}"
