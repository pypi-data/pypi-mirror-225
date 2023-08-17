from .gui.screens import *
from .gui.screens.screen import *
from .gui.elements import *
from .flows.flow import Flow
from .server import Server
from .util import Settings
from .flowmatic import App


server = Server()


def run(app: App):
    """Start app.
    Args:
        screen (type[Screen]): Screen to start with."""
    server.app = app
    server.app.start()


def get_app() -> App:
    return server.app


def set_start_screen(screen_t: type[Screen]):
    """Set start screen.
    Args:
        screen (type[Screen]): Screen to start with."""
    screen = screen_t()
    server.app.start_screen = screen
    server.app.gui.start_screen = screen


def show_start_screen():
    """Show start screen."""
    server.app.show_start_screen()


def show_screen(screen: Screen):
    """Show screen.
    Args:
        screen (type[Screen]): Screen to show."""
    server.app.show_screen(screen)


def show_error(error: Exception | str):
    server.app.gui.show_error(error)


def start_flow(flow: Flow):
    """Start flow.
    Args:
        flow (Flow): Flow to start."""
    server.app.start_flow(flow)


def get_settings() -> Settings:
    """Get settings.
    Returns:
        Settings: Settings."""
    return server.app.settings


def set_settings(settings: dict[str, str]) -> None:
    """Set settings.
    Args:
        settings (dict[str, str]): Settings."""
    server.app.settings.set(settings)
    server.app.settings.save()


def file_dialog(
    title: str, max_files: int, filetypes: list[tuple[str, str]]
) -> tuple[str, ...]:
    """Open file dialog.
    Args:
        title (str): Title.
        max_files (int): Max files.
        filetypes (list[tuple[str, str]]): Filetypes.
    Returns:
        str | None: File path."""
    return server.app.file_dialog(title, max_files, filetypes)


def update_gui():
    server.app.gui.update()


def quit_app():
    server.app.quit()
