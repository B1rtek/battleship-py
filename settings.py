from enum import Enum


class Setting(Enum):
    MARK_MISSES_AROUND = 0


class Settings:
    """
    Class handling setting settings
    """

    def __init__(self):
        """
        Sets default settings
        """
        self._settings = {
            Setting.MARK_MISSES_AROUND: True
        }

    def set_mark_misses_around(self, new_state: bool):
        """
        Toggles the "Mark misses around sunken ships" setting
        """
        self._settings[Setting.MARK_MISSES_AROUND] = new_state

    def get_settings(self) -> dict:
        return self._settings
