from pathlib import Path

from pcsFilter.file_handling.file_finder import file_from_path
from pcsFilter.quality_handler import QualityHandler
from pcsFilter.tools.black import run_black
from pcsFilter.tools.blue import run_blue
from pcsFilter.tools.flake8 import run_flake8
from pcsFilter.tools.isort import run_isort
from pcsFilter.tools.radon import run_radon

VERSION_ONE_PLUS = False


def _prepare_for_analysis(output_path: Path) -> None:
    """
    1. Clean up analysis logs before tests
    2. Create output folder if missing

    :param output_path:
    """
    file_from_path(path=output_path / 'flake8.txt').delete()
    file_from_path(path=output_path / 'radon.json').delete()

    output_path.mkdir(parents=True, exist_ok=True)


def run_all(path: str, output_path: str, strict: bool):
    """Run all pcsFilter steps against given path

    :param strict:
    :param path:
    :param output_path:
    """
    output_path = Path(output_path)
    _prepare_for_analysis(output_path)
    if VERSION_ONE_PLUS:
        run_black(path)
    run_blue(path)
    run_isort(path)
    run_flake8(path, output_path)
    run_radon(path, output_path)
    QualityHandler(path, output_path, strict).compare_metrics()
