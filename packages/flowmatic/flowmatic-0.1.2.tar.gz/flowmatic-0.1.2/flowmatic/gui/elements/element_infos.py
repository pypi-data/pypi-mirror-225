from typing import Callable, NamedTuple


Element = NamedTuple


class Button(NamedTuple):
    text: str
    command: Callable[[], None]


class Info(Element):
    label: str
    value: str


class InfoFrame(Element):
    title: str
    rows: list[Info]
