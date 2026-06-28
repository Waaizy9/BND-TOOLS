"""Tests for BND.lib.updater — update helpers, file skipping, zip root."""
import os
import tempfile

import pytest

from BND.lib import constants as C
from BND.lib.updater import (
    PRESERVE_VOID,
    _find_zip_root,
    _s,
    _skip_void_file,
    _void_rel,
    _zip_url,
)


class TestStrings:
    def test_german_strings(self):
        result = _s("title", de=True)
        assert result == "AKTUALISIERUNG ERFORDERLICH"

    def test_english_strings(self):
        result = _s("title", de=False)
        assert result == "UPDATE REQUIRED"

    def test_all_keys_have_both_languages(self):
        from BND.lib.updater import _STRINGS
        for key, val in _STRINGS.items():
            assert len(val) == 2, f"Key {key} should have DE and EN strings"
            assert isinstance(val[0], str)
            assert isinstance(val[1], str)


class TestVoidRel:
    def test_basic_relative_path(self):
        rel = _void_rel("/root/bnd/config/settings.json", "/root/bnd")
        assert rel == os.path.normpath("config/settings.json")

    def test_same_dir(self):
        rel = _void_rel("/root/bnd/file.py", "/root/bnd")
        assert rel == "file.py"


class TestSkipVoidFile:
    def test_settings_json_is_preserved(self):
        rel = os.path.normpath("config/settings.json")
        assert _skip_void_file(rel) is True

    def test_nuker_json_is_preserved(self):
        rel = os.path.normpath("config/discord-nuker.json")
        assert _skip_void_file(rel) is True

    def test_data_dir_is_skipped(self):
        assert _skip_void_file("data") is True

    def test_data_subdir_is_skipped(self):
        rel = os.path.join("data", "cache.json")
        assert _skip_void_file(rel) is True

    def test_normal_file_not_skipped(self):
        assert _skip_void_file("lib/search.py") is False

    def test_config_dir_not_skipped(self):
        assert _skip_void_file("config") is False

    def test_other_config_file_not_skipped(self):
        rel = os.path.normpath("config/remote-manifest.json")
        assert _skip_void_file(rel) is False

    def test_lib_file_not_skipped(self):
        assert _skip_void_file("lib/constants.py") is False


class TestFindZipRoot:
    def test_single_dir_with_bnd(self, tmp_path):
        root = tmp_path / "BND-TOOLS-main"
        bnd = root / "BND"
        bnd.mkdir(parents=True)
        (bnd / "main.py").write_text("pass")

        result = _find_zip_root(str(tmp_path))
        assert result == str(root)

    def test_bnd_directly_in_dir(self, tmp_path):
        bnd = tmp_path / "BND"
        bnd.mkdir()
        (bnd / "main.py").write_text("pass")

        result = _find_zip_root(str(tmp_path))
        assert result == str(tmp_path)

    def test_no_bnd_folder(self, tmp_path):
        (tmp_path / "other").mkdir()
        (tmp_path / "other" / "file.py").write_text("pass")

        result = _find_zip_root(str(tmp_path))
        assert result is None

    def test_nested_dir_with_bnd(self, tmp_path):
        nested = tmp_path / "archive"
        bnd = nested / "BND"
        bnd.mkdir(parents=True)
        (bnd / "main.py").write_text("pass")

        result = _find_zip_root(str(tmp_path))
        assert result == str(nested)

    def test_ignores_dotfiles(self, tmp_path):
        (tmp_path / ".git").mkdir()
        bnd = tmp_path / "BND"
        bnd.mkdir()

        result = _find_zip_root(str(tmp_path))
        assert result == str(tmp_path)

    def test_empty_dir(self, tmp_path):
        result = _find_zip_root(str(tmp_path))
        assert result is None


class TestZipUrl:
    def test_returns_github_zip_url(self, tmp_config_dir, reset_settings, monkeypatch):
        from BND.lib import remote
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {
            "config_rev": "0",
            "latest_version": "2.0.0",
            "links": {"github": "https://github.com/waaizy9/BND-TOOLS"},
        })
        url = _zip_url()
        assert url.endswith(".zip")
        assert "github.com" in url

    def test_uses_direct_zip_url_if_present(self, tmp_config_dir, reset_settings, monkeypatch):
        from BND.lib import remote
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {
            "zip_url": "https://github.com/waaizy9/BND-TOOLS/archive/refs/heads/main.zip",
            "links": {},
        })
        url = _zip_url()
        assert url == "https://github.com/waaizy9/BND-TOOLS/archive/refs/heads/main.zip"

    def test_fallback_to_constant(self, tmp_config_dir, reset_settings, monkeypatch):
        from BND.lib import remote
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"links": {}})
        url = _zip_url()
        assert "github.com" in url
        assert url.endswith(".zip")


class TestPreserveVoid:
    def test_settings_in_preserve(self):
        assert os.path.normpath("config/settings.json") in PRESERVE_VOID

    def test_nuker_in_preserve(self):
        assert os.path.normpath("config/discord-nuker.json") in PRESERVE_VOID
