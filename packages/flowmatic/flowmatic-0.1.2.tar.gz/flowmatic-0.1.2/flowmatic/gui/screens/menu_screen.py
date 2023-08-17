import customtkinter as ctk

from flowmatic import gui
from flowmatic.gui.screens.screen import Screen
from ...gui.elements import Button


class MenuScreen(Screen):
    """Menu screen. Used for menus.

    Args:
        master (tk.Tk): Master window."""

    def build(  # pylint: disable=arguments-differ
        self, title: str, buttons: list[Button]
    ) -> None:
        """Build screen.

        Args:
            title (str): Title of screen.
            buttons (list[gui.ButtonInfo]): List of buttons to add to screen."""
        ctk.CTkLabel(self.master, text=title).pack(**gui.pack_defaults)
        for button in buttons:
            ctk.CTkButton(self.master, text=button.text, command=button.command).pack(
                **gui.pack_defaults
            )
