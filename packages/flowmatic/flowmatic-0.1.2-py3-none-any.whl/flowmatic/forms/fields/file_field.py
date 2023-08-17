import os
import platform
import tkinter as tk
from typing import Iterable, Literal, Self

import customtkinter as ctk
from PIL import Image
from tkinterdnd2 import DND_FILES

import flowmatic
from flowmatic import gui
from flowmatic.util import Icons
from flowmatic.util.exceptions import TooManyFilesError

MAX_COLUMNS = 4
IMAGE_WIDTH = 130


class FileField:
    master: tk.Frame
    frame: tk.Frame
    label: str
    __value: list[str]
    __msg: tk.StringVar
    max_files: int
    width: int
    height: int
    drop_frame: ctk.CTkFrame
    image_width: int = IMAGE_WIDTH
    columns: int
    rows: int

    @property
    def value(self) -> list[str]:
        return self.files

    @value.setter
    def value(self, value) -> None:
        pass

    @property
    def files(self) -> list[str]:
        return self.__value.copy()

    @files.setter
    def files(self, value: list[str]) -> None:
        if len(value) > self.max_files:
            raise TooManyFilesError(self.max_files)
        self.__value = value

    @property
    def message(self) -> str:
        return self.__msg.get()

    @message.setter
    def message(self, value: str) -> None:
        self.__msg.set(value)

    def __init__(
        self,
        label: str,
        *,
        max_files: int = 1,
        files: list[str] | None = None,
    ) -> None:
        self.label = label
        self.__value = files or []
        self.__msg = tk.StringVar(value="")
        self.max_files = max_files if max_files >= 1 else 1
        self.columns = MAX_COLUMNS if self.max_files > MAX_COLUMNS else self.max_files
        self.rows = (self.max_files - 1) // MAX_COLUMNS + 1
        self.width = (
            self.columns * self.image_width
            if self.max_files < 4
            else 4 * self.image_width
        )
        self.height = self.rows * self.image_width

    def __call__(self, master: tk.Frame) -> Self:
        self.master = master
        self.frame = ctk.CTkFrame(
            self.master,
            height=self.height,
            fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
        )
        return self

    def get(self) -> list[str]:
        return self.files

    def build(self, method: Literal["pack"] = "pack", **kwargs) -> Self:
        match method:
            case _:
                build_method = self.pack
        self.frame.pack()
        build_method(
            ctk.CTkLabel(master=self.frame, text=self.label), side=tk.LEFT, **kwargs
        )

        kwargs.pop("expand", True)
        self.drop_frame = ctk.CTkFrame(
            self.frame,
            width=self.width,
            height=self.height,
        )
        build_method(
            self.drop_frame,
            propagate=False,
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=False,
            **kwargs,
        )
        self.drop_frame.drop_target_register(DND_FILES)  # type: ignore # pylint: disable=no-member
        self.drop_frame.dnd_bind("<<Drop>>", lambda file: self.add_file(file.data.strip("{}")))  # type: ignore  # pylint: disable=no-member
        # Message
        build_method(
            ctk.CTkLabel(self.master, textvariable=self.__msg), **gui.pack_defaults
        )

        button_frame = ctk.CTkFrame(
            self.frame, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )
        build_method(button_frame, side=tk.RIGHT, **kwargs)

        if platform.system() != "Darwin":
            ctk.CTkButton(
                button_frame,
                text="Browse",
                command=lambda: self.add_files(
                    flowmatic.file_dialog(
                        title="Select File",
                        max_files=self.max_files,
                        filetypes=[("All Files", "*.*")],
                    )
                ),
            ).pack(**kwargs)

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_files,
        ).pack(**kwargs)

        return self

    def pack(self, element: tk.Widget, **kwargs) -> None:
        if kwargs.pop("propagate", None) is False:
            element.pack_propagate(False)
            element.grid_propagate(False)
        element.pack(**kwargs)

    def add_files(self, files: Iterable[str]) -> None:
        for file in files:
            self.add_file(file)

    def add_file(self, file: str) -> None:
        try:
            self.files += [file]
        except TooManyFilesError as exc:
            self.message = str(exc)
        else:
            self.message = ""
            file_frame = ctk.CTkFrame(
                self.drop_frame,
                width=self.image_width,
                height=self.image_width,
                fg_color=ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"],
            )
            index = len(self.files) - 1
            column, row = self.get_position(index)
            file_frame.grid(column=column, row=row)
            file_frame.master.grid_columnconfigure(column, weight=1)

            your_image = ctk.CTkImage(
                light_image=Image.open(
                    os.path.join(Icons.path, Icons.get_icon(file.lower()))
                ),
                size=(72, 97),
            )
            ctk.CTkLabel(master=file_frame, image=your_image, text="").pack(expand=True)
            ctk.CTkLabel(file_frame, text=os.path.split(file)[-1]).pack(
                **gui.pack_defaults
            )

    def get_position(self, index: int) -> tuple[int, int]:
        column = index % self.columns
        row = index // self.columns
        return column, row

    def clear_files(self) -> None:
        self.files = []
        self.message = ""
        for widget in self.drop_frame.winfo_children():
            widget.destroy()
        # flowmatic.update_gui()
