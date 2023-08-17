from .gui import GUI, TKGUI
from .gui.screens.screen import Screen
from .util.settings import Settings
from .util.user import User
from .flows.flow import Flow


class App:
    """Singleton for accessing GUI, settings, user and other app-wide objects.

    Attributes:
        gui (GUI): GUI interface.
        settings (Settings): Settings.
        user (User): User.

    Args:
        title (str, optional): Title of the app. Defaults to "Appy".
    """

    title: str = "FlowMatic"
    gui: GUI = None  # type: ignore
    settings: Settings
    user: User

    start_screen: Screen

    def __init__(self, start_screen: type[Screen]):
        self.gui = self.gui or TKGUI(
            title=self.title, start_screen=start_screen, geometry="1280x720"
        )
        self.start_screen = start_screen()
        self.settings = Settings.load("files/settings.json")
        self.user = User("")

    def start(self, start_screen: Screen | None = None):
        """Start app.
        Args:
            screen (type[Screen]): Screen to start with."""
        self.gui.start(start_screen)

    def show_start_screen(self):
        """Show start screen."""
        self.gui.switch_screen(self.start_screen)

    def show_screen(self, screen: Screen):
        """Show start screen.
        Args:
            screen (type[Screen]): Screen to show."""
        self.gui.switch_screen(screen)

    def start_flow(self, flow: Flow):
        """Start flow.
        Args:
            flow (type[Flow]): Flow to start."""
        self.gui.start_flow(flow)

    def file_dialog(
        self, title: str, max_files: int, filetypes: list[tuple[str, str]]
    ) -> tuple[str, ...]:
        """Open file dialog.
        Args:
            title (str): Title of the dialog.
            max_files (int): Maximum number of files to select.
            filetypes (list[tuple[str, str]]): Filetypes to show.
        Returns:
            str | None: Path to file or None if no file selected."""
        filenames = self.gui.file_dialog(title, max_files, filetypes)

        if not filenames:
            return ("",)

        if isinstance(filenames, str):
            return (filenames,)

        return filenames

    def quit(self):
        self.gui.quit()
