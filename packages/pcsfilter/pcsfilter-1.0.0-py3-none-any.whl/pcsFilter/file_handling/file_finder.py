from pathlib import Path

from pcsFilter.file_handling.abstract_file_handler import AFileHandler
from pcsFilter.file_handling.existing_file import ExistingFile
from pcsFilter.file_handling.non_existing_file import NonExistingFile


def file_from_path(path: Path) -> AFileHandler:
    """Find file by given path and return it in the form of AFileHandler

    :param path:
    :return:
    """
    try:
        return ExistingFile(Path(path))
    except (StopIteration, FileNotFoundError):
        return NonExistingFile(str(path))


def file_from_same_dir(name: str) -> AFileHandler:
    """
    Find file in the current directory
    and return it in the form of AFileHandler
    """
    relative_file_path = Path('') / name
    return file_from_path(relative_file_path)
