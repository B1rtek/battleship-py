import json
import os
from enum import Enum
from json import JSONDecodeError


class Setting(Enum):
    MARK_MISSES_AROUND = 0,
    HARD_ENEMY = 1


class Settings:
    """
    Class handling setting settings
    """

    def __init__(self, path: str = "settings.json"):
        """
        Initializes settings by loading the default ones
        :param path: path to the settings file
        :type path: str
        """
        self._default_settings = {
            Setting.MARK_MISSES_AROUND: True,
            Setting.HARD_ENEMY: False
        }
        self._path = path
        self._settings = self._default_settings

    def set_mark_misses_around(self, new_state: bool):
        """
        Toggles the "Mark misses around sunken ships" setting
        """
        self._settings[Setting.MARK_MISSES_AROUND] = new_state

    def set_hard_enemy(self, new_state: bool):
        """
        Toggles the "Harder enemy" setting
        """
        self._settings[Setting.HARD_ENEMY] = new_state

    def load_settings(self):
        """
        Loads settings from the specified settings file
        """
        if not os.path.exists(self._path):
            return
        else:
            try:
                with open(self._path, 'r') as file_handle:
                    settings_json = json.load(file_handle)
                    self._settings[Setting.MARK_MISSES_AROUND] = settings_json[
                        "mark_misses_around"]
                    self._settings[Setting.HARD_ENEMY] = settings_json[
                        "hard_enemy"]
            except (JSONDecodeError, PermissionError, KeyError):
                return

    def save_settings(self):
        """
        Saves settings to the specified settings file
        """
        try:
            with open(self._path, 'w') as file_handle:
                settings_dict = {
                    "mark_misses_around": self._settings[
                        Setting.MARK_MISSES_AROUND],
                    "hard_enemy": self._settings[Setting.HARD_ENEMY]
                }
                json.dump(settings_dict, file_handle, indent=4)
        except PermissionError:
            return

    def get_settings(self) -> dict:
        return self._settings
