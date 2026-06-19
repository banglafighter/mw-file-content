import yaml
from mw_common.mw_exception import MwException
from mw_file_content.content.mwfc_content_util import ContentUtil


class DataFileUtil:

    @staticmethod
    def read_yaml(file_path: str, exception_message: str = "Invalid File", raise_exception: bool = True, default=None):
        yaml_content = ContentUtil.read_text_file(file_path, exception_message=exception_message, raise_exception=raise_exception, default=default)
        try:
            if yaml_content:
                return yaml.safe_load(yaml_content)
        except Exception as e:
            if raise_exception:
                raise MwException(f"{exception_message}: {e}")
        return default
