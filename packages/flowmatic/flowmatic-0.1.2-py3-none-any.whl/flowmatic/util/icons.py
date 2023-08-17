from enum import StrEnum


class Icons(StrEnum):
    CODE = "Code.png"
    FILE = "File.png"
    FOLDER = "Folder.png"
    IMAGE = "Image.png"
    PDF = "PDF.png"
    TEXT = "Text.png"
    TABLE = "Table.png"
    ZIP = "Zip.png"

    @classmethod
    def get_icon(cls, file: str) -> str:
        extension = file.split(".")[-1]
        match extension:
            case "py" | "html" | "css" | "js" | "json" | "xml" | "yaml" | "yml":
                return cls.CODE
            case "pdf":
                return cls.PDF
            case "zip" | "rar" | "7z" | "tar" | "gz" | "xz" | "bz2":
                return cls.ZIP
            case "png" | "jpg" | "jpeg" | "gif" | "svg" | "ico" | "bmp" | "webp":
                return cls.IMAGE
            case "txt" | "md" | "rst" | "doc" | "docx" | "odt" | "rtf" | "tex" | "wpd" | "wps" | "odt":  # pylint: disable=line-too-long
                return cls.TEXT
            case "csv" | "tsv" | "xls" | "xlsx" | "ods":
                return cls.TABLE
            case _:
                return cls.FILE

    @classmethod
    @property
    def path(cls) -> str:
        return "assets/icons"
