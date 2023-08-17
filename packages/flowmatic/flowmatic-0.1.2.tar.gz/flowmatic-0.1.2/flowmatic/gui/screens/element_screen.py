import customtkinter as ctk
import tkinter as tk
from flowmatic import gui
from flowmatic.gui.elements.element_infos import *  # pylint: disable=wildcard-import, unused-wildcard-import
from flowmatic.gui.screens.screen import Screen


class ElementScreen(Screen):
    def build(  # pylint: disable=arguments-differ
        self, elements: list[Element], **kwargs
    ) -> None:
        for element in elements:
            self.build_element(element, self.master, **kwargs)

    @classmethod
    def build_element(
        cls, element: Element, master: tk.Frame | tk.Tk, **kwargs
    ) -> None:
        match element:
            case Button():
                ctk.CTkButton(master, text=element.text, command=element.command).pack(
                    **(gui.pack_defaults | kwargs),
                )
            case Info():
                ctk.CTkLabel(
                    master,
                    text=f"{element.label}: {element.value}",
                ).pack(**(gui.pack_defaults | kwargs))
            case InfoFrame():
                frame = ctk.CTkFrame(master)
                frame.pack(**gui.pack_defaults)
                ctk.CTkLabel(frame, text=element.title).pack(
                    **(gui.pack_defaults | kwargs),
                )
                for row in element.rows:
                    cls.build_element(row, frame, **kwargs)
            case _:
                raise NotImplementedError(
                    f"Unknown element type: {element.__class__.__name__}, extend ElementScreen.build_element() to support it."
                )
