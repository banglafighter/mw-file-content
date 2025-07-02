import zipfile
from datetime import datetime
import os
import shutil
from pathlib import Path
from mw_common.mw_exception import MwException


class FileUtil:
    @staticmethod
    def is_exist(path: str):
        return os.path.exists(path)

    @staticmethod
    def is_it_file(path: str):
        return os.path.isfile(path)

    @staticmethod
    def is_it_dir(path: str):
        return os.path.isdir(path)

    @staticmethod
    def get_file_extension(filename: str):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower()
        return None

    @staticmethod
    def remove_file_extension(name_with_extension: str):
        return Path(name_with_extension).stem

    @staticmethod
    def get_filename_from_path(path_with_filename: str):
        path_with_filename = path_with_filename.rstrip(os.sep)
        filename = os.path.basename(path_with_filename)
        return filename

    @staticmethod
    def delete(path: str):
        if FileUtil.is_exist(path):
            if FileUtil.is_it_file(path):
                os.remove(path)
            elif FileUtil.is_it_dir(path):
                shutil.rmtree(path, ignore_errors=True)
            else:
                return False
        return True

    @staticmethod
    def create_directories(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def rename(source: str, destination: str):
        os.rename(source, destination)

    @staticmethod
    def copy(source: str, destination: str, ignore_copy=None):
        # ignore_copy = shutil.ignore_patterns("*.pyc", "__pycache__"), any `*.pyc` files or __pycache__ directories will not be copied.
        if os.path.isdir(source):
            return shutil.copytree(source, destination, ignore_copy)
        else:
            return shutil.copy(source, destination)

    @staticmethod
    def join_path(*args):
        return os.path.join(*args)

    @staticmethod
    def get_current_path():
        return os.getcwd()

    @staticmethod
    def file_size_into_byte(path):
        if FileUtil.is_exist(path):
            return os.stat(path).st_size
        return None

    @staticmethod
    def get_created_modified_datetime(path):
        if not FileUtil.is_exist(path):
            return None, None
        load_file_path = Path(path)
        create_timestamp = load_file_path.stat().st_ctime
        modify_timestamp = load_file_path.stat().st_mtime
        return datetime.fromtimestamp(create_timestamp), datetime.fromtimestamp(modify_timestamp)

    @staticmethod
    def create_empty_file(path):
        try:
            with open(path, "x") as empty:
                empty.close()
                return True
        except FileExistsError:
            return False

    @staticmethod
    def get_human_readable_file_size(size):
        B = float(size)
        KB = float(1024)
        MB = float(KB ** 2)
        GB = float(KB ** 3)
        TB = float(KB ** 4)

        if B < KB:
            return '{0} {1}'.format(B, 'B' if 0 == B > 1 else 'B')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)
        return None

    @staticmethod
    def create_zip(source: str, zip_file_path: str):
        source = os.path.abspath(source)
        zip_file_path = os.path.abspath(zip_file_path)

        if not os.path.exists(source):
            raise MwException(f"Source path does not exist: {source}")

        if os.path.exists(zip_file_path):
            raise MwException(f"Zip file already exists: {zip_file_path}")

        # Create zip safely using context manager
        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for dirpath, _, filenames in os.walk(source):
                for filename in filenames:
                    abs_file_path = os.path.abspath(os.path.join(dirpath, filename))
                    arcname = os.path.relpath(abs_file_path, source)
                    zip_file.write(abs_file_path, arcname)
