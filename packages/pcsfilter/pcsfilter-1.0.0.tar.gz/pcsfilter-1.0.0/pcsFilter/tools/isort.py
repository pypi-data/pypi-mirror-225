"""
Use the same approach as in isort tests
https://github.com/PyCQA/isort/blob/main/tests/unit/test_main.py#L86
"""

from isort import main


def run_isort(dir_path: str) -> None:
    main.main([dir_path])
