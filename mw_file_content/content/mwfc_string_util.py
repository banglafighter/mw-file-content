import re
from copy import copy


class StringUtil:

    @classmethod
    def find_and_replace_with(cls, text: str, find: any, replace: any):
        text = copy(text)
        return text.replace(find, replace)

    @classmethod
    def lower_first_char(cls, text: str) -> str:
        return text[0].lower() + text[1:] if text else ""

    @classmethod
    def camelcase_to(cls, text: str, to: str = "_") -> str:
        text = text.strip()
        return re.sub(r'(?<!^)(?=[A-Z])', to, text)

    @classmethod
    def replace_multiple_occurrence_to_single_with(cls, text: str, to: str = "_") -> str:
        return re.sub(f"{re.escape(to)}+", to, text)

    @classmethod
    def system_readable(cls, text: str) -> str:
        text = StringUtil.camelcase_to(text, "_")
        text = StringUtil.find_and_replace_with(text, " ", "_")
        text = StringUtil.find_and_replace_with(text, "-", "_")
        text = StringUtil.replace_multiple_occurrence_to_single_with(text, "_")
        text = re.sub(r'[^a-zA-Z0-9_]', '', text)
        return text.strip().lower()

    @classmethod
    def remove_special_character(cls, text: str, to: str = "") -> str:
        return re.sub(r'[^\w\s/\-\u0980-\u09FF]', to, text)

    @classmethod
    def remove_leading_number(cls, text: str) -> str:
        return re.sub(r"^\d+", '', text)

    @classmethod
    def py_underscore_name(cls, name: str) -> str:
        name = StringUtil.lower_first_char(name)
        name = StringUtil.system_readable(name)
        name = StringUtil.remove_special_character(name)
        name = StringUtil.remove_leading_number(name)
        return name

    @classmethod
    def replace_space_with(cls, text: str, to: str = "_"):
        return re.sub(r'\s+', to, text)

    @classmethod
    def human_readable(cls, text: str, default=None):
        if text is None:
            return default
        text = StringUtil.camelcase_to(copy(text), " ")
        text = StringUtil.find_and_replace_with(text, "-", " ")
        text = text.strip()
        text = text.title()
        return StringUtil.replace_space_with(text, " ")

    @classmethod
    def text_to_url_text(cls, text: str, default=None):
        if not text:
            return default
        text = cls.camelcase_to(copy(text), "-")
        text = cls.find_and_replace_with(text, " ", "-")
        text = cls.find_and_replace_with(text, "_", "-")
        text = cls.replace_multiple_occurrence_to_single_with(text=text, to="-")
        text = cls.remove_special_character(text)
        text = text.strip()
        text = text.strip("-")
        text = text.lower()
        return text

    @classmethod
    def pad_zero(cls, number: int, width: int = 2) -> str:
        return f"{number:0{width}d}"

    @classmethod
    def py_hyphen_name(cls, name: str):
        name = cls.py_underscore_name(name=name)
        name = cls.find_and_replace_with(text=name, find="_", replace="-")
        return name

    @classmethod
    def _to_words(cls, text: str) -> list[str]:
        if not text:
            return []
        processed = text.replace('&', ' and ')
        processed = re.sub(r'([a-z])([A-Z])', r'\1 \2', processed)
        processed = re.sub(r'[^a-zA-Z0-9]', ' ', processed)
        return [word for word in processed.lower().split() if word]

    @classmethod
    def to_hyphen_case(cls, text: str) -> str:
        return '-'.join(cls._to_words(text))

    @classmethod
    def to_kabab_case(cls, text: str) -> str:
        return cls.to_hyphen_case(text)

    @classmethod
    def to_underscore_case(cls, text: str) -> str:
        return '_'.join(cls._to_words(text))

    @classmethod
    def to_snake_case(cls, text: str) -> str:
        return cls.to_underscore_case(text)

    @classmethod
    def to_camel_case(cls, text: str) -> str:
        words = cls._to_words(text)
        if not words:
            return ''
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @classmethod
    def to_pascal_case(cls, text: str) -> str:
        return ''.join(word.capitalize() for word in cls._to_words(text))

    @classmethod
    def to_title_case(cls, text: str) -> str:
        return ' '.join(word.capitalize() for word in cls._to_words(text))

    @classmethod
    def to_sentence_case(cls, text: str) -> str:
        words = cls._to_words(text)
        if not words:
            return ''
        sentence = ' '.join(words)
        return sentence.capitalize()

    @classmethod
    def to_schema_column_name_snake_case(cls, text: str, default_value: str = "") -> str:
        if not text:
            return default_value

        parts = text.split('.')
        transformed_parts = []

        for part in parts:
            processed = re.sub(r'([a-z])([A-Z])', r'\1 \2', part)
            processed = re.sub(r'[^a-zA-Z0-9]', ' ', processed)
            words = [word for word in processed.lower().split() if word]
            transformed_parts.append('_'.join(words))
        return '.'.join(transformed_parts)
