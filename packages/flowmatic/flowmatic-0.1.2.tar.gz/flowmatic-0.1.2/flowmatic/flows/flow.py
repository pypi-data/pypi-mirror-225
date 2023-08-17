from __future__ import annotations
from typing import TYPE_CHECKING, Protocol

import flowmatic

if TYPE_CHECKING:
    from flowmatic.gui.screens.screen import FlowScreen, Screen


class Flow(Protocol):
    steps: list[type[FlowScreen]]
    screens: list[FlowScreen]
    return_to: Screen
    step: int

    def __init__(self) -> None:
        self.screens = [screen(self) for screen in self.steps]
        self.step = 0

    def __next__(self) -> None:
        if self.step == len(self.screens) or self.step < 0:
            flowmatic.show_screen(self.return_to)
            return
        screen = self.screens[self.step]
        self.step += 1
        flowmatic.show_screen(screen)

    def start(self):
        next(self)

    def quit(self):
        self.step = len(self.screens)
        next(self)

    def next(self):
        next(self)

    def previous(self):
        self.step -= 2
        next(self)
