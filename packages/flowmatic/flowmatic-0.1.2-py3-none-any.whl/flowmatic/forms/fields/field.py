from typing import Any, Protocol, Self
import tkinter as tk


class Field(Protocol):
    master: tk.Frame
    label: str
    __value: Any

    @property
    def value(self) -> int | str | list[str] | None:
        return self.__value

    @value.setter
    def value(self, value: Any) -> None:
        self.__value = value

    def __init__(
        self,
        label: str,
    ) -> None:
        ...

    def __call__(self, master: tk.Frame) -> Self:
        ...

    def build(self) -> Self:
        ...

    def pack(  # pylint: disable=missing-function-docstring
        self, element: tk.Widget, **kwargs: dict[str, Any]
    ) -> None:
        ...
