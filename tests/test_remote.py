"""Tests for BND.lib.remote — manifest helpers, rev parsing, overrides."""
import json
import os

import pytest

from BND.lib import constants as C
from BND.lib import remote


class TestRevNum:
    def test_valid_rev(self):
        assert remote._rev_num({"config_rev": "5"}) == 5

    def test_rev_as_int(self):
        assert remote._rev_num({"config_rev": 10}) == 10

    def test_missing_rev(self):
        assert remote._rev_num({}) == 0

    def test_none_manifest(self):
        assert remote._rev_num(None) == 0

    def test_invalid_rev(self):
        assert remote._rev_num({"config_rev": "abc"}) == 0

    def test_zero_rev(self):
        assert remote._rev_num({"config_rev": "0"}) == 0


class TestApplyOverrides:
    def test_applies_discord_link(self, monkeypatch):
        original_discord = C.DISCORD
        manifest = {"links": {"discord": "https://discord.gg/test123"}}
        remote.apply_overrides(manifest)
        assert C.DISCORD == "https://discord.gg/test123"
        C.DISCORD = original_discord

    def test_applies_github_link(self, monkeypatch):
        original = C.GITHUB
        manifest = {"links": {"github": "https://github.com/test/repo"}}
        remote.apply_overrides(manifest)
        assert C.GITHUB == "https://github.com/test/repo"
        C.GITHUB = original

    def test_applies_shop_link(self, monkeypatch):
        original = C.SHOP
        manifest = {"links": {"shop": "https://shop.example.com"}}
        remote.apply_overrides(manifest)
        assert C.SHOP == "https://shop.example.com"
        C.SHOP = original

    def test_applies_changelog(self, monkeypatch):
        original = C.CHANGELOG
        manifest = {"links": {}, "changelog": "New changelog text"}
        remote.apply_overrides(manifest)
        assert C.CHANGELOG == "New changelog text"
        C.CHANGELOG = original

    def test_empty_links_no_change(self):
        original = C.DISCORD
        manifest = {"links": {}}
        remote.apply_overrides(manifest)
        assert C.DISCORD == original

    def test_none_links_no_crash(self):
        manifest = {"links": None}
        remote.apply_overrides(manifest)  # should not raise

    def test_missing_links_no_crash(self):
        manifest = {}
        remote.apply_overrides(manifest)  # should not raise


class TestDefaultManifest:
    def test_returns_dict(self, tmp_config_dir):
        result = remote._default_manifest()
        assert isinstance(result, dict)

    def test_has_config_rev(self, tmp_config_dir):
        result = remote._default_manifest()
        assert "config_rev" in result

    def test_has_latest_version(self, tmp_config_dir):
        result = remote._default_manifest()
        assert "latest_version" in result

    def test_loads_from_local_file(self, tmp_config_dir):
        manifest_path = os.path.join(C.CONFIG_DIR, "remote-manifest.json")
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, "w") as f:
            json.dump({"config_rev": "42", "latest_version": "3.0.0", "links": {}}, f)

        monkeypatch_path = manifest_path
        original = remote.LOCAL_MANIFEST
        remote.LOCAL_MANIFEST = manifest_path
        result = remote._default_manifest()
        remote.LOCAL_MANIFEST = original
        assert result["config_rev"] == "42"


class TestConfigRev:
    def test_returns_string(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"config_rev": "7"})
        assert remote.config_rev() == "7"

    def test_missing_rev_returns_zero(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {})
        assert remote.config_rev() == "0"


class TestVersionUpdateAvailable:
    def test_same_version_no_update(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": C.VERSION})
        assert remote.version_update_available() is False

    def test_newer_version_available(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": "99.0.0"})
        assert remote.version_update_available() is True

    def test_older_version_no_update(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": "0.0.1"})
        assert remote.version_update_available() is False


class TestStatusBadge:
    def test_no_updates_empty_badge(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": C.VERSION, "config_rev": "0"})
        from BND.lib.config import get_settings
        s = get_settings()
        s.set("last_seen_config_rev", "0")
        assert remote.status_badge() == ""

    def test_version_update_shows_maj(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": "99.0.0"})
        assert remote.status_badge() == "MAJ"

    def test_pending_config_shows_new(self, tmp_config_dir, reset_settings, monkeypatch):
        monkeypatch.setattr(remote, "_loaded", True)
        monkeypatch.setattr(remote, "_manifest", {"latest_version": C.VERSION, "config_rev": "5"})
        from BND.lib.config import get_settings
        s = get_settings()
        s.set("last_seen_config_rev", "0")
        assert remote.status_badge() == "NEW"


class TestFetchUrl:
    def test_adds_cache_buster(self):
        url = "https://example.com/file.json"
        sep = "&" if "?" in url else "?"
        busted = f"{url}{sep}t="
        assert busted.startswith("https://example.com/file.json?t=")

    def test_cache_buster_with_existing_params(self):
        url = "https://example.com/file.json?a=1"
        sep = "&" if "?" in url else "?"
        assert sep == "&"
