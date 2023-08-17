from typing import Tuple
import customtkinter as ctk
import tkinterdnd2
import tkinter.filedialog as tkfd
from CTkMessagebox import CTkMessagebox


from flowmatic.gui.gui import GUI  # pylint: disable=import-error

from .screens.screen import Screen
from ..flows.flow import Flow


class CustomTk(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        ctk.CTk.__init__(self, fg_color=fg_color, **kwargs)
        self.TkdndVersion = tkinterdnd2.TkinterDnD._require(self)


class TKGUI(GUI):
    root: CustomTk
    title: str
    start_screen: Screen
    geometry: str
    light_mode: bool

    def __init__(
        self,
        title: str,
        start_screen: type[Screen],
        geometry: str = "1280x720",
        light_mode: bool = False,
    ) -> None:
        self.root = CustomTk()
        self.title = title
        self.start_screen = start_screen()
        self.geometry = geometry
        self.light_mode = light_mode

    def start(self, start_screen: Screen | None) -> None:
        """Start GUI.
        Args:
            screen (type[Screen]): Screen to start with."""
        self.setup()
        self.build_screen(start_screen or self.start_screen)
        self.root.mainloop()

    def setup(self) -> None:
        ctk.set_appearance_mode("light" if self.light_mode else "dark")
        self.root.geometry(self.geometry)
        self.root.title(self.title)
        self.root.resizable(False, False)
        self.root.focus_set()
        self.root.configure(bg=ctk.ThemeManager.theme["CTk"]["fg_color"])

    def file_dialog(
        self, title: str, max_files: int, filetypes: list[tuple[str, str]]
    ) -> str | tuple[str, ...]:
        """Open file dialog.
        Args:
            title (str): Title of the dialog.
            max_files (int): Maximum number of files to select.
            filetypes (list[tuple[str, str]]): Filetypes to show.
        Returns:
            str | None: Path to file or None if no file selected."""
        if max_files == 1:
            return tkfd.askopenfilename(title=title, filetypes=filetypes)
        return tkfd.askopenfilenames(title=title, filetypes=filetypes)

    def start_flow(self, flow: Flow) -> None:
        self.clear_screen()
        self.current_flow = flow
        flow.start()

    def switch_screen(self, screen: Screen) -> None:
        """Switch to a new screen.

        Args:
            screen (type[Screen]): Screen to show."""
        self.clear_screen()
        self.build_screen(screen)

    def build_screen(self, screen: Screen) -> None:
        """Build screen.

        Args:
            screen (type[Screen]): Screen to build."""
        screen(self.root).build()
        self.current_screen = screen

    def clear_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_error(self, error: Exception | str) -> None:
        CTkMessagebox(title="Error", message=f"{error}", icon="cancel")

    def update(self) -> None:
        self.root.update()

    def quit(self) -> None:
        self.root.quit()
