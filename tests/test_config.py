"""Tests for BND.lib.config — settings load/save and nuker status."""
import json
import os

import pytest

from BND.lib import constants as C
from BND.lib.config import DEFAULTS, Settings, get_settings, nuker_status


class TestDefaults:
    def test_defaults_has_language(self):
        assert "language" in DEFAULTS

    def test_defaults_has_theme(self):
        assert "theme" in DEFAULTS

    def test_defaults_has_username(self):
        assert "username" in DEFAULTS

    def test_defaults_has_skip_boot(self):
        assert "skip_boot" in DEFAULTS


class TestSettings:
    def test_fresh_settings_uses_defaults(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.data["language"] == DEFAULTS["language"]
        assert s.data["theme"] == DEFAULTS["theme"]
        assert s.data["username"] == DEFAULTS["username"]

    def test_get_existing_key(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.get("language") == DEFAULTS["language"]

    def test_get_missing_key_returns_default(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.get("nonexistent_key", "fallback") == "fallback"

    def test_get_missing_key_uses_defaults_dict(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.get("username") == DEFAULTS["username"]

    def test_set_key(self, tmp_config_dir, reset_settings):
        s = Settings()
        s.set("username", "TestUser")
        assert s.data["username"] == "TestUser"

    def test_set_theme_applies_theme(self, tmp_config_dir, reset_settings):
        s = Settings()
        s.set("theme", "blue")
        assert C._ACTIVE_THEME == "blue"

    def test_save_creates_file(self, tmp_config_dir, reset_settings):
        s = Settings()
        s.set("username", "SaveTest")
        s.save()
        assert os.path.isfile(C.SETTINGS_PATH)
        with open(C.SETTINGS_PATH) as f:
            data = json.load(f)
        assert data["username"] == "SaveTest"

    def test_load_reads_saved_data(self, tmp_config_dir, reset_settings):
        s1 = Settings()
        s1.set("username", "LoadTest")
        s1.save()

        s2 = Settings()
        assert s2.get("username") == "LoadTest"

    def test_load_merges_with_defaults(self, tmp_config_dir, reset_settings):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.SETTINGS_PATH, "w") as f:
            json.dump({"username": "Custom"}, f)

        s = Settings()
        assert s.get("username") == "Custom"
        assert s.get("language") == DEFAULTS["language"]

    def test_load_handles_corrupt_json(self, tmp_config_dir, reset_settings):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.SETTINGS_PATH, "w") as f:
            f.write("{invalid json")

        s = Settings()
        assert s.data == dict(DEFAULTS)

    def test_lang_property(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.lang == DEFAULTS["language"]

    def test_username_property(self, tmp_config_dir, reset_settings):
        s = Settings()
        assert s.username == DEFAULTS["username"]

    def test_lang_property_after_set(self, tmp_config_dir, reset_settings):
        s = Settings()
        s.set("language", "en")
        assert s.lang == "en"


class TestGetSettings:
    def test_singleton(self, tmp_config_dir, reset_settings):
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2

    def test_returns_settings_instance(self, tmp_config_dir, reset_settings):
        s = get_settings()
        assert isinstance(s, Settings)


class TestNukerStatus:
    def test_no_config_file(self, tmp_config_dir):
        has_token, has_server = nuker_status()
        assert has_token is False
        assert has_server is False

    def test_empty_config(self, tmp_config_dir):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.NUKER_CFG_PATH, "w") as f:
            json.dump({}, f)
        has_token, has_server = nuker_status()
        assert has_token is False
        assert has_server is False

    def test_valid_config(self, tmp_config_dir):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.NUKER_CFG_PATH, "w") as f:
            json.dump({"token": "abc123", "server_id": "456"}, f)
        has_token, has_server = nuker_status()
        assert has_token is True
        assert has_server is True

    def test_partial_config_token_only(self, tmp_config_dir):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.NUKER_CFG_PATH, "w") as f:
            json.dump({"token": "abc123"}, f)
        has_token, has_server = nuker_status()
        assert has_token is True
        assert has_server is False

    def test_corrupt_config(self, tmp_config_dir):
        os.makedirs(C.CONFIG_DIR, exist_ok=True)
        with open(C.NUKER_CFG_PATH, "w") as f:
            f.write("{bad json")
        has_token, has_server = nuker_status()
        assert has_token is False
        assert has_server is False
