import tkinter as tk
from typing import Any, Self

import customtkinter as ctk

from flowmatic import gui


class RadioGroup:
    master: tk.Frame
    frame: tk.Frame
    label: str
    __value: tk.StringVar
    options: list[str]

    @property
    def value(self) -> str:
        return self.__value.get()

    @value.setter
    def value(self, value: str) -> None:
        self.__value.set(value)

    def __init__(
        self,
        label: str,
        value: str | None = None,
        options: list[str] | None = None,
    ) -> None:
        self.label = label
        self.__value = tk.StringVar(value=value)
        self.options = options or []

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
        for option in self.options:
            ctk.CTkRadioButton(
                self.frame, text=option, variable=self.__value, value=option
            ).pack(side=tk.LEFT, **kwargs)
        return self

    def pack(self, element: tk.Widget, **kwargs) -> None:
        element.pack(**kwargs)
