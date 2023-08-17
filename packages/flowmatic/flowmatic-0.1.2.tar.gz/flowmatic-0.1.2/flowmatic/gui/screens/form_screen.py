import tkinter as tk
from typing import Callable, TypeVar, overload

import customtkinter as ctk

import flowmatic
from flowmatic import gui
from flowmatic.flows.flow import Flow
from flowmatic.gui.screens.screen import FlowScreen, Screen
from ...forms import FormValidation
from ...forms.fields.field import Field
from ..elements.element_infos import Button

T = TypeVar("T")


class FormScreen(Screen):
    field_list: list[Field] | None
    fields: dict[str, Field]
    validations: list[FormValidation] | None = None
    __message: tk.StringVar

    @property
    def message(self) -> str:
        return self.__message.get()

    @message.setter
    def message(self, value: str) -> None:
        """Set message.

        Args:
            value (str): Message."""
        self.__message.set(value)

    def __init__(
        self,
    ) -> None:
        self.fields = {}
        self.__message = tk.StringVar(value="")

    @property
    def values(self) -> dict[str, str | int | list[str]]:
        """Get values from fields.

        Returns:
            dict[str, str]: Values from fields."""
        return {
            label: field.value for label, field in self.fields.items() if field.value
        }

    def validate(self) -> None:
        if not self.validations:
            return

        for validation in self.validations:
            validation.validate(self.values)

    @overload
    def get(self, __key: str, /) -> str | int | list[str]:
        ...

    @overload
    def get(self, __key: str, __default: T) -> str | int | list[str] | T:
        ...

    @overload
    def get(self, __key: str, __default: T, __return: type[T]) -> T:
        ...

    def get(
        self, __key: str, __default: str | T = "", __return: type[T] | None = None
    ) -> str | int | list[str] | T:
        """Get value from field.

        Args:
            label (str): Label of field.

        Returns:
            str: Value of field."""
        value = self.values.get(__key, __default)
        if __return is not None:
            if not isinstance(value, __return):
                raise TypeError(f"Expected {__return} got {type(value)}")
        return value

    def submit_default(self) -> None:
        flowmatic.show_start_screen

    def build(  # pylint: disable=arguments-differ
        self,
        *,
        title: str,
        validations: list[FormValidation] | None = None,
        submit_button: Button | None = None,
        back_button: Button | None = None,
        fields: list[Field] | None = None,
        field_factory: Callable[..., list[Field]] | None = None,
    ) -> None:
        """Build screen.

        Args:

            title (str): Title of screen.
            validate_command (Callable[[], None]): Command to run when validate button is pressed.
            validate_text (str, optional): Text of validate button. Defaults to "Submit".
            back_command (Callable[[], None], optional): Command to run when back button is pressed.
                 Defaults to None.
        """
        # Variables
        self.field_list = (fields or []) + (field_factory() if field_factory else [])
        self.validations = validations
        if not submit_button:
            submit_button = Button(text="Submit", command=self.submit_default)

        def validate_command() -> None:
            try:
                self.validate()
            except AssertionError as error:
                self.message = str(error)
                flowmatic.update_gui()
            else:
                submit_button.command()

        # Title
        ctk.CTkLabel(self.master, text=title).pack(**gui.pack_defaults)

        # Fields
        if self.field_list:
            fields_frame = (
                ctk.CTkScrollableFrame(
                    self.master, height=gui.HEIGHT - 150, width=gui.WIDTH
                )
                if not isinstance(self.master, ctk.CTkScrollableFrame)
                else ctk.CTkFrame(self.master)
            )
            fields_frame.pack(**gui.pack_defaults)
            for field in self.field_list:
                self.fields[field.label] = field(fields_frame).build(
                    **gui.pack_defaults
                )

        # Message
        ctk.CTkLabel(self.master, textvariable=self.__message).pack(**gui.pack_defaults)

        # Buttons
        pack_args = gui.pack_defaults  # | {"pady": (10, 20)}
        button_frame = ctk.CTkFrame(self.master)
        button_frame.pack(**pack_args)
        ctk.CTkButton(
            button_frame, text=submit_button.text or "Submit", command=validate_command
        ).pack(**gui.pack_defaults, side=tk.RIGHT)
        if back_button:
            ctk.CTkButton(
                button_frame,
                text=back_button.text or "Back",
                command=back_button.command,
            ).pack(**gui.pack_defaults, side=tk.LEFT)


class FlowFormScreen(FormScreen, FlowScreen):
    def __init__(self, flow: Flow) -> None:
        self.flow = flow
        super().__init__()
