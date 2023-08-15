"""
Call radon mi() command
"""
from pathlib import Path

import radon.cli as cli


def run_radon(dir_path: str, output_path: Path):
    output_file = str(output_path / 'radon.txt')
    cli.cc(
        paths=[dir_path],
        no_assert=True,
        total_average=True,
        order='ALPHA',
        output_file=output_file,
    )
