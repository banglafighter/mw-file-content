from copy import copy


class StringUtil:

    @staticmethod
    def find_and_replace_with(text: str, find: any, replace: any):
        text = copy(text)
        return text.replace(find, replace)
