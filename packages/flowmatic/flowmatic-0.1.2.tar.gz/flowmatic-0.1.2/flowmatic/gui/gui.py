from typing import Protocol
from .screens.screen import Screen
from ..flows.flow import Flow


class GUI(Protocol):
    title: str
    start_screen: Screen
    current_screen: Screen
    current_flow: Flow

    def __init__(self, title: str, start_screen: Screen):
        ...

    def start(self, start_screen: Screen | None):
        ...

    def setup(self):
        ...

    def switch_screen(self, screen: Screen):
        ...

    def start_flow(self, flow: Flow):
        ...

    def build_screen(self, screen: Screen):
        ...

    def clear_screen(self):
        ...

    def file_dialog(
        self, title: str, max_files: int, filetypes: list[tuple[str, str]]
    ) -> str | tuple[str, ...]:
        ...

    def show_error(self, error: Exception | str) -> None:
        ...

    def update(self):
        ...

    def quit(self):
        ...
