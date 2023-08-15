import configparser
from pathlib import Path
from typing import Optional

from configupdater import ConfigUpdater

from pcsFilter.file_handling.file_finder import file_from_path

SECTION_NAME = 'pcsFilter'
NEW_CONFIG_FILE = (
    "[pcsFilter]\n# Goal is '0'\nflake8 = -1\n# Goal is '0'\ncc = -1\n"
)


class SetUpHandler:
    """Handle setup.cfg"""

    def __init__(self, output_path: Path):
        self._output_path = output_path
        self.config = configparser.ConfigParser(allow_no_value=True)
        self._load_config_file()
        self.c_updater = ConfigUpdater()
        self.c_updater.read(self.config_file.file_path())

    def _load_config_file(self):
        self._try_load_setup_cfg()
        self._create_setup_cfg_if_not_exists()

    def _create_setup_cfg_if_not_exists(self):
        if not self.config_file.exists():
            self.config_file = self.config_file.write(NEW_CONFIG_FILE)

    def _try_load_setup_cfg(self):
        path = self._output_path / 'setup.cfg'
        self.config_file = file_from_path(path=path)

    def has_section(self, section: str) -> bool:
        """
        :return: True if no properties found. Else False
        """
        return self.c_updater.has_section(section)

    def save(self):
        """Save all given values to setup.cfg"""
        self.c_updater.write(self.config_file.writable_file())

    def get(self, param: str) -> Optional[str]:
        """Get param from 'pcsFilter' section

        :param param:
        :return: param value or None
        """
        option = self.c_updater.get(
            section=SECTION_NAME,
            option=param,
            fallback=None,
        )
        if option is None:
            return None
        else:
            return option.value

    def set(self, param: str, value: str) -> None:
        """Set 'pcsFilter' param with given value

        :param param:
        :param value:
        """
        self.c_updater[SECTION_NAME][param].value = value
