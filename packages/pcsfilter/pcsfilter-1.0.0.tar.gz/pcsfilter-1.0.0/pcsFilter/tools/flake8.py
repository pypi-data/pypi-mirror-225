"""
Use the same approach as in flake8 tests
https://github.com/PyCQA/flake8/blob/main/tests/integration/test_main.py#L15
"""
from pathlib import Path

from flake8.main import cli


def run_flake8(path: str, output_path: Path) -> None:
    output_file = str(output_path / 'flake8.txt')
    try:
        cli.main([path, f'--output-file={output_file}'])
    except SystemExit:
        pass  # expected exception
