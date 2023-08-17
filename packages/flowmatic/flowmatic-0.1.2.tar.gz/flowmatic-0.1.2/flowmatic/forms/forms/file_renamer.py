import os
from flowmatic import FormScreen
from flowmatic.forms import TextField, RadioGroup, FileField
import flowmatic


class FileRenamer(FormScreen):
    base_path: str

    def __init__(self, path: str) -> None:
        self.base_path = path
        super().__init__()

    def build(self) -> None:  # pylint: disable=arguments-differ
        return super().build(
            title="Save File",
            on_submit=self.save,
            back_command=flowmatic.show_start_screen,
            fields=[
                TextField(label="Name", placeholder_text="file.txt"),
                RadioGroup(
                    label="File Type",
                    options=["Text File", "Binary File"],
                    value="Text File",
                ),
                FileField(label="File"),
            ],
        )

    def save(self):
        files: list[str] = self.get("File", [], list)
        if not files:
            self.message = "No file selected"
        old_path = files[0]  # pylint: disable=unsubscriptable-object

        new_name = self.get("Name", "", str)
        if not new_name:
            self.message = "Name cannot be empty"
            return

        new_path = os.path.join(self.base_path, new_name)
        os.rename(old_path, new_path)
        flowmatic.show_start_screen()
