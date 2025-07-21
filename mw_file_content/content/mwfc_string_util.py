import re
from copy import copy


class StringUtil:

    @staticmethod
    def find_and_replace_with(text: str, find: any, replace: any):
        text = copy(text)
        return text.replace(find, replace)

    @staticmethod
    def lower_first_char(text: str) -> str:
        return text[0].lower() + text[1:] if text else ""

    @staticmethod
    def camelcase_to(text: str, to: str = "_") -> str:
        text = text.strip()
        return re.sub(r'(?<!^)(?=[A-Z])', to, text)

    @staticmethod
    def replace_multiple_occurrence_to_single_with(text: str, to: str = "_") -> str:
        return re.sub(f"{re.escape(to)}+", to, text)

    @staticmethod
    def system_readable(text: str) -> str:
        text = StringUtil.camelcase_to(text, "_")
        text = StringUtil.find_and_replace_with(text, " ", "_")
        text = StringUtil.find_and_replace_with(text, "-", "_")
        text = StringUtil.replace_multiple_occurrence_to_single_with(text, "_")
        text = re.sub(r'[^a-zA-Z0-9_]', '', text)
        return text.strip().lower()

    @staticmethod
    def remove_special_character(text: str, to: str = "") -> str:
        return re.sub(r'[^\w\s/\-]', to, text)

    @staticmethod
    def remove_leading_number(text: str) -> str:
        return re.sub(r"^\d+", '', text)

    @staticmethod
    def py_underscore_name(name: str) -> str:
        name = StringUtil.lower_first_char(name)
        name = StringUtil.system_readable(name)
        name = StringUtil.remove_special_character(name)
        name = StringUtil.remove_leading_number(name)
        return name

    @staticmethod
    def replace_space_with(text: str, to: str = "_"):
        return re.sub(r'\s+', to, text)

    @staticmethod
    def human_readable(text: str, default=None):
        if text is None:
            return default
        text = StringUtil.camelcase_to(copy(text), " ")
        text = StringUtil.find_and_replace_with(text, "-", " ")
        text = text.strip()
        text = text.title()
        return StringUtil.replace_space_with(text, " ")
