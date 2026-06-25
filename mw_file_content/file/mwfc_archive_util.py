from mw_common import MwException
import io
import os
import zipfile
from pathlib import Path


class Archive:

    @classmethod
    def create_zip(cls, source: str | Path, zip_file_path: str | Path | None = None, *, overwrite: bool = False, return_bytes: bool = False, compression_level: int = 9 ) -> str | bytes:
        source = Path(source).resolve()
        if not source.exists():
            raise MwException(f"Source path does not exist: {source}")

        if return_bytes:
            buffer = io.BytesIO()

            with zipfile.ZipFile(
                    buffer,
                    mode="w",
                    compression=zipfile.ZIP_DEFLATED,
                    compresslevel=compression_level
            ) as zip_file:
                cls._add_source_to_zip(zip_file, source)
            return buffer.getvalue()

        if zip_file_path is None:
            raise MwException("zip_file_path is required when return_bytes=False")

        zip_file_path = cls._normalize_zip_path(zip_file_path)
        if zip_file_path.exists() and not overwrite:
            raise MwException(f"Zip file already exists: {zip_file_path}")

        zip_file_path.parent.mkdir(parents=True,exist_ok=True)

        with zipfile.ZipFile(
                zip_file_path,
                mode="w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=compression_level
        ) as zip_file:
            cls._add_source_to_zip(zip_file, source)
        return str(zip_file_path)

    @classmethod
    def _normalize_zip_path(cls, zip_file_path: str | Path) -> Path:
        zip_file_path = Path(zip_file_path)
        if zip_file_path.suffix.lower() != ".zip":
            zip_file_path = zip_file_path.with_suffix(".zip")
        return zip_file_path.resolve()

    @classmethod
    def extract_zip(cls, zip_source: str | Path | bytes, destination: str | Path, *, overwrite: bool = False) -> str:
        destination = Path(destination).resolve()

        if destination.exists():
            if any(destination.iterdir()) and not overwrite:
                raise MwException(f"Destination directory is not empty: {destination}")
        else:
            destination.mkdir(parents=True, exist_ok=True)

        if isinstance(zip_source, bytes):
            zip_stream = io.BytesIO(zip_source)
            with zipfile.ZipFile(zip_stream, "r") as zip_file:
                cls._safe_extract(zip_file, destination)
        else:
            zip_source = Path(zip_source).resolve()
            if not zip_source.exists():
                raise MwException(f"Zip file does not exist: {zip_source}")

            with zipfile.ZipFile(zip_source, "r") as zip_file:
                cls._safe_extract(zip_file, destination)

        return str(destination)

    @classmethod
    def _add_source_to_zip(cls, zip_file: zipfile.ZipFile, source: Path) -> None:
        if source.is_file():
            zip_file.write(source, arcname=source.name)
            return

        for dirpath, dirnames, filenames in os.walk(source):
            dirpath = Path(dirpath)

            if not dirnames and not filenames:
                relative_dir = dirpath.relative_to(source)
                zip_info = zipfile.ZipInfo(f"{relative_dir.as_posix()}/")
                zip_file.writestr(zip_info, "")

            for filename in filenames:
                file_path = dirpath / filename
                arcname = file_path.relative_to(source)
                zip_file.write(file_path, arcname=arcname)

    @classmethod
    def _safe_extract(cls, zip_file: zipfile.ZipFile, destination: Path) -> None:
        destination = destination.resolve()
        for member in zip_file.namelist():
            target = (destination / member).resolve()

            if not str(target).startswith(str(destination)):
                raise MwException(f"Unsafe zip entry detected: {member}")
        zip_file.extractall(destination)