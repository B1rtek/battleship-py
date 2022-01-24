import json
import os

from settings import Settings, Setting


def test_settings_create():
    settings = Settings()
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert not setts[Setting.HARD_ENEMY]


def test_settings_set_mark_misses_around():
    settings = Settings()
    settings.set_mark_misses_around(False)
    setts = settings.get_settings()
    assert not setts[Setting.MARK_MISSES_AROUND]
    assert not setts[Setting.HARD_ENEMY]


def test_settings_set_hard_enemy():
    settings = Settings()
    settings.set_hard_enemy(True)
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert setts[Setting.HARD_ENEMY]


def test_settings_load_settings_no_settings_file():
    assert not os.path.exists("non_existent.json")
    settings = Settings("non_existent.json")
    settings.load_settings()
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert not setts[Setting.HARD_ENEMY]
    assert not os.path.exists("non_existent.json")


def test_settings_load_settings_malformed_json():
    with open("test.json", 'w') as file_handle:
        file_handle.write("something that is not a json")
    settings = Settings("test.json")
    settings.load_settings()
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert not setts[Setting.HARD_ENEMY]
    os.remove("test.json")


def test_settings_load_settings_wrong_keys():
    with open("test.json", 'w') as file_handle:
        file_handle.write("{\"invalid_key\": true}")
    settings = Settings("test.json")
    settings.load_settings()
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert not setts[Setting.HARD_ENEMY]
    os.remove("test.json")


def test_settings_save_settings():
    assert not os.path.exists("test.json")
    settings = Settings("test.json")
    settings.set_hard_enemy(True)
    setts = settings.get_settings()
    assert setts[Setting.MARK_MISSES_AROUND]
    assert setts[Setting.HARD_ENEMY]
    settings.save_settings()
    assert os.path.exists("test.json")
    with open("test.json", 'r') as file_handle:
        json_setts = json.load(file_handle)
        assert json_setts["mark_misses_around"]
        assert json_setts["hard_enemy"]
    os.remove("test.json")
