import customtkinter as ctk

from flowmatic import gui
from flowmatic.gui.screens.screen import Screen
from ...gui.elements import Button


class TitleScreen(Screen):
    """Title screen.

    Args:
        master (tk.Tk): Master of screen."""

    def build(  # pylint: disable=arguments-differ
        self, title: str, button: Button
    ) -> None:
        """Build screen.

        Args:
            title (str): Title of screen.
            button (gui.ButtonInfo): Button to show.
        """
        ctk.CTkLabel(self.master, text=title).pack(**gui.pack_defaults)
        ctk.CTkButton(self.master, text=button[0], command=button[1]).pack(
            **gui.pack_defaults,
        )
