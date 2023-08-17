from typing import Protocol, Self
import tkinter as tk
import customtkinter as ctk

from ...flows.flow import Flow
from flowmatic import gui

TOPBAR_HEIGHT = 100
SIDEBAR_WIDTH = 200


class Screen(Protocol):
    """Screen protocol.

    Args:
        master (tk.Tk): Master window.

    Methods:
        build: Build screen."""

    master: tk.Tk | tk.Frame

    def __init__(self) -> None:
        ...

    def __call__(self, master: tk.Tk | tk.Frame) -> Self:
        self.master = master  # pylint: disable=attribute-defined-outside-init
        return self

    def build(self) -> None:  # pylint: disable=missing-function-docstring
        ...


class FlowScreen(Screen):
    flow: Flow

    def __init__(self, flow: Flow) -> None:
        self.flow = flow
        super().__init__()

    def next(self) -> None:
        self.flow.next()

    def previous(self) -> None:
        self.flow.previous()

    def build(self) -> None:
        raise NotImplementedError


class WrappedScreen(Screen):
    screens: list[Screen]
    inner: type[Screen]
    sidebar: type[Screen] | None = None
    topbar: type[Screen] | None = None

    def __init__(self) -> None:
        self.screens = []

    def __call__(self, master: tk.Tk) -> Self:
        self.master = master
        outer_frame = ctk.CTkFrame(master)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        inner_frame = ctk.CTkScrollableFrame(
            outer_frame,
            width=gui.WIDTH - SIDEBAR_WIDTH,
            height=gui.HEIGHT - TOPBAR_HEIGHT,
        )
        self.screens.append(self.inner()(inner_frame))
        if self.sidebar is not None:
            side_frame = ctk.CTkFrame(outer_frame, width=SIDEBAR_WIDTH)
            side_frame.pack(side=tk.LEFT)
            self.screens.append(self.sidebar()(side_frame))
        if self.topbar is not None:
            top_frame = ctk.CTkFrame(outer_frame, height=TOPBAR_HEIGHT)
            top_frame.pack(side=tk.TOP)
            self.screens.append(self.topbar()(top_frame))

        inner_frame.pack()
        return self

    def build(self) -> None:
        for screen in self.screens:
            screen.build()
