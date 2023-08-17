from abc import ABC
import json
from typing import Any, Self

from flowmatic.util.exceptions import SavedClassLoadException


class SavedClass(ABC):
    def __init__(self, path: str):
        self.path = path

    def set(self, kwargs: dict[str, Any]) -> Self:
        """Set attributes.

        Args:
            kwargs (dict[str, Any]): Attributes to set.

        Returns:
            Self: Self."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    def items(self):
        _dict = self.__dict__.copy()
        _dict.pop("path")
        return _dict.items()

    def save(self):
        if self.path:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(self.__dict__, fp=file)

    def load_from_disk(self) -> None:
        with open(self.path, "r", encoding="utf-8") as file:
            try:
                json_data = json.load(file)
                for key, value in json_data.items():
                    setattr(self, key, value)
            except Exception as exc:
                raise SavedClassLoadException(self.path) from exc

    def create_file(self) -> None:
        f = open(self.path, "w", encoding="utf-8")
        f.close()

    @classmethod
    def load(cls, path: str) -> Self:
        """Load the class from disk.

        Args:
            path (str): Path to load from.

        Returns:
            Self: The loaded class.

        Raises:
            SavedClassLoadException: If the class could not be loaded."""
        self = cls(path)
        try:
            self.load_from_disk()
        except FileNotFoundError:
            self.create_file()

        return self
