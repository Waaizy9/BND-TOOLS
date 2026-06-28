"""Shared fixtures for BND-TOOLS tests."""
import json
import os
import sys
import tempfile

import pytest

# Ensure BND package is importable
_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _repo not in sys.path:
    sys.path.insert(0, _repo)


@pytest.fixture()
def tmp_config_dir(tmp_path, monkeypatch):
    """Redirect all BND config/data paths to a temp directory."""
    from BND.lib import constants as C

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    monkeypatch.setattr(C, "CONFIG_DIR", str(config_dir))
    monkeypatch.setattr(C, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(C, "SETTINGS_PATH", str(config_dir / "settings.json"))
    monkeypatch.setattr(C, "NUKER_CFG_PATH", str(config_dir / "discord-nuker.json"))
    monkeypatch.setattr(C, "CUSTOM_TOOLS_DIR", str(tmp_path / "custom"))

    return tmp_path


@pytest.fixture()
def reset_settings(monkeypatch):
    """Reset the settings singleton between tests."""
    import BND.lib.config as cfg

    monkeypatch.setattr(cfg, "_settings", None)
