from typing import Callable, Any


class FormValidation:
    field_label: str
    condition: Callable[[Any], bool]
    message: str

    def __init__(
        self, field_label: str, condition: Callable[[Any], bool], message: str
    ) -> None:
        self.field_label = field_label
        self.condition = condition
        self.message = message

    def validate(self, values: dict[str, int | str | list[str]] | None) -> None:
        assert values, "Form is empty."
        value = values.get(self.field_label, None)
        assert value is not None, f"{self.field_label} is empty."
        assert self.condition(value), f"{self.field_label}: {self.message}"
