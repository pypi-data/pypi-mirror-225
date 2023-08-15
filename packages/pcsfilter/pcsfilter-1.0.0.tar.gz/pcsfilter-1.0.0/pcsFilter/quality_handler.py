import re
import sys
from pathlib import Path

import click

from pcsFilter.file_handling.file_finder import file_from_path
from pcsFilter.setup_handler import SetUpHandler

FLAKE_8_MESSAGE = (
    'Flake8 score was {init_flake8} '
    'but became {new_flake8}. '
    'You have introduced new pip8 error(s). '
    'Please check flake8.txt for details. '
    'Please fix all new and maybe some old errors.\n\n'
)

RADON_MESSAGE = (
    'Radon cyclomatic complexity was {init_cc} '
    'but became {new_cc}. '
    'You have made code less maintainable. '
    'Please check radon.txt for details. '
    'Please improve maintainability back. '
    'Appreciate if you make it even better.\n\n'
)


class QualityHandler:
    """Handle quality metrics"""

    def __init__(self, path: str, output_path: Path, strict: bool):
        self._output_message = ''
        self._output_path = output_path
        self._path = path
        self.strict = strict

    def compare_metrics(self):
        """Compare initial metrics with new metrics"""
        self._count_new_flake8_flags()
        self._calculate_new_cc_stats()
        self._load_previous_metrics()
        self._compare_flake8()
        self._compare_cc()
        self._echo_pcsFilter_message()
        self._save_result()

    def _count_new_flake8_flags(self):
        last_line_does_not_count = 1
        flake8_content = self._load_content(file_name='flake8.txt')
        self.new_flake8 = (
            len(flake8_content.split('\n')) - last_line_does_not_count
        )

    def _calculate_new_cc_stats(self):
        radon_content = self._load_content(file_name='radon.txt')
        self.new_cc = 0

        for line in radon_content.split('\n'):
            if 'Average complexity' in line:
                self.new_cc = re.search(r'\((.*)\)', line).group(1)

    def _load_previous_metrics(self):
        self.setup = SetUpHandler(output_path=self._output_path)
        self.init_flake8 = self._load_init_value('flake8')
        self.init_cc = self._load_init_value('cc')

    def _load_init_value(self, key: str):
        value = self.setup.get(key)
        if value == '-1':
            return None
        else:
            return value

    def _load_content(self, file_name: str):
        wrapped_path = self._output_path / file_name
        file_content = file_from_path(wrapped_path).get_content()
        return file_content

    def _compare_flake8(self):
        if self.init_flake8 is not None and int(self.init_flake8) < int(
            self.new_flake8
        ):
            self._output_message += FLAKE_8_MESSAGE.format(
                init_flake8=self.init_flake8,
                new_flake8=self.new_flake8,
            )

    def _compare_cc(self):
        if self.init_cc is not None and float(self.init_cc) < float(
            self.new_cc
        ):
            self._output_message += RADON_MESSAGE.format(
                init_cc=self.init_cc,
                new_cc=self.new_cc,
            )

    def _echo_pcsFilter_message(self):  # noqa
        if self._output_message:
            click.echo(self._output_message)
            if self.strict:
                sys.exit(1)

    def _save_result(self):
        self.setup.set('flake8', str(self.new_flake8))
        self.setup.set('cc', str(self.new_cc))
        self.setup.save()
