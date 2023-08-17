import tkinter as tk
from typing import Any, Self

import customtkinter as ctk

from flowmatic import gui


class CheckBox:
    master: tk.Frame
    frame: tk.Frame
    label: str
    __value: tk.BooleanVar
    show: bool

    @property
    def value(self) -> bool:
        return self.__value.get()

    @value.setter
    def value(self, value: bool) -> None:
        self.__value.set(value)

    def __init__(
        self,
        label: str,
        *,
        value: bool | None = None,
    ) -> None:
        self.label = label
        self.__value = tk.BooleanVar(value=value)

    def __call__(self, master: tk.Frame) -> Self:
        self.master = master
        self.frame = ctk.CTkFrame(
            self.master,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
        )
        return self

    def build(self, **kwargs: dict[str, Any]) -> Self:
        self.frame.pack(**gui.pack_defaults)
        ctk.CTkLabel(master=self.frame, text=self.label).pack(side=tk.LEFT, **kwargs)
        ctk.CTkCheckBox(self.frame, variable=self.__value).pack(side="left", **kwargs)
        return self

    def pack(self, element: tk.Widget, **kwargs) -> None:
        element.pack(**kwargs)
