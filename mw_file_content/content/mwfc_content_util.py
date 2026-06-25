from pathlib import Path
from mw_common import MwException
from ..common.mw_file_content_data import FindReplaceData


class ContentUtil:
    @staticmethod
    def read_text_file(file_path: str, exception_message: str = "Invalid File", raise_exception: bool = True, default=None) -> str | None:
        path = Path(file_path)

        if not path.exists():
            if raise_exception:
                raise MwException(exception_message)
            return default

        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            if raise_exception:
                raise MwException(f"{exception_message}: {e}")
            return default

    @staticmethod
    def write_text_to_file(file_path: str, text_content: str) -> bool:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()  # delete existing file

            with path.open('w', encoding='utf-8') as file:
                file.write(text_content)
            return True
        except Exception:
            return False

    @staticmethod
    def insert_text_in_file_at_index(file_path: str, index: int, text_content: str) -> bool:
        try:
            path = Path(file_path)
            with path.open('r+', encoding='utf-8') as stream:
                lines = stream.readlines()
                lines.insert(index, text_content)
                stream.seek(0)
                stream.writelines(lines)
            return True
        except Exception:
            return False

    @staticmethod
    def find_and_replace_in_file(file_path: str, find_replace_data: list[FindReplaceData]):
        text_content = ContentUtil.read_text_file(file_path)
        if text_content:
            for find_replace in find_replace_data:
                if find_replace.find is not None and find_replace.replace is not None:
                    text_content = text_content.replace(find_replace.find, find_replace.replace)
            ContentUtil.write_text_to_file(file_path, text_content)
