import tkinter as tk
from typing import Any, Self
import customtkinter as ctk
from flowmatic import gui
from flowmatic.gui.elements.element_infos import Element


class Display:
    master: tk.Frame
    frame: tk.Frame
    label: str
    __value: None = None
    elements: list[Element]

    @property
    def value(self) -> None:
        return self.__value

    @value.setter
    def value(self, value) -> None:
        pass

    def __init__(self, label: str, elements: list[Element] | None = None) -> None:
        self.label = label
        self.elements = elements or []

    def __call__(
        self,
        master: tk.Frame,
    ) -> Self:
        self.master = master
        self.frame = ctk.CTkFrame(
            self.master,
            # fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
        )
        return self

    def build(self, **kwargs: dict[str, Any]) -> Self:
        self.frame.pack()
        ctk.CTkLabel(self.frame, text=self.label).pack(**gui.pack_defaults)
        for element in self.elements:
            gui.screens.ElementScreen.build_element(element, self.frame)
        return self

    def pack(self, element: tk.Widget, **kwargs) -> None:
        element.pack(**kwargs)
