"""
Use the same approach as in black tests
https://github.com/psf/black/blob/b1d060101626aa1c332f52e4bdf0ae5e4cc07990/tests/test_black.py#L2203
"""
import subprocess


def run_blue(path: str) -> None:
    subprocess.run(['blue', path], check=True)
