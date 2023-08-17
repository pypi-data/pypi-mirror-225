import tkinter as tk
from typing import Any, Self

import customtkinter as ctk


class TextField:
    master: tk.Frame
    frame: tk.Frame
    label: str
    __value: tk.StringVar
    placeholder_text: str | None
    show: bool

    @property
    def value(self) -> str:
        return self.__value.get()

    @value.setter
    def value(self, value: str) -> None:
        self.__value.set(value)

    def __init__(
        self,
        label: str,
        *,
        value: str | None = None,
        placeholder_text: str | None = None,
        show: bool = True
    ) -> None:
        self.label = label
        self.__value = tk.StringVar(value=value)
        self.placeholder_text = placeholder_text
        self.show = show

    def __call__(self, master: tk.Frame) -> Self:
        self.master = master
        self.frame = ctk.CTkFrame(
            self.master,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
        )
        return self

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, TextField):
            return False
        return self.value == __value.value and self.label == __value.label

    def build(self, **kwargs: dict[str, Any]) -> Self:
        self.frame.pack()
        ctk.CTkLabel(master=self.frame, text=self.label).pack(side=tk.LEFT, **kwargs)
        entry = ctk.CTkEntry(
            self.frame,
            textvariable=self.__value,
            placeholder_text=self.placeholder_text,
            show="•" if not self.show else None,
        )
        entry.pack(side=tk.RIGHT, **kwargs)
        return self

    def pack(self, element: tk.Widget, **kwargs) -> None:
        element.pack(**kwargs)
