"""
Use the same approach as in black tests
https://github.com/psf/black/blob/b1d060101626aa1c332f52e4bdf0ae5e4cc07990/tests/test_black.py#L2203
"""

import black
from click.testing import CliRunner


def run_black(path: str) -> None:
    CliRunner().invoke(black.main, [path])
