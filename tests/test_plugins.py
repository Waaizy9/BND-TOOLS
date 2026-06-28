"""Tests for BND.lib.plugins — plugin discovery."""
import os

import pytest

from BND.lib import constants as C
from BND.lib.plugins import discover_plugins


class TestDiscoverPlugins:
    def test_empty_directory(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        plugins = discover_plugins()
        assert plugins == []

    def test_discovers_python_files(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "my_tool.py"), "w")).close()
        plugins = discover_plugins()
        assert len(plugins) == 1
        assert plugins[0][0] == "P01"
        assert "My Tool" in plugins[0][1]
        assert "[PLUGIN]" in plugins[0][1]

    def test_ignores_underscore_files(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "_private.py"), "w")).close()
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "__init__.py"), "w")).close()
        plugins = discover_plugins()
        assert plugins == []

    def test_multiple_plugins_sorted(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        for name in ("beta_tool.py", "alpha_tool.py", "charlie_tool.py"):
            (open(os.path.join(C.CUSTOM_TOOLS_DIR, name), "w")).close()
        plugins = discover_plugins()
        assert len(plugins) == 3
        codes = [p[0] for p in plugins]
        assert codes == ["P01", "P02", "P03"]

    def test_label_formatting(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "my-cool-tool.py"), "w")).close()
        plugins = discover_plugins()
        assert "My Cool Tool" in plugins[0][1]

    def test_creates_dir_if_missing(self, tmp_config_dir):
        if os.path.exists(C.CUSTOM_TOOLS_DIR):
            os.rmdir(C.CUSTOM_TOOLS_DIR)
        discover_plugins()
        assert os.path.isdir(C.CUSTOM_TOOLS_DIR)

    def test_ignores_non_python_files(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "readme.txt"), "w")).close()
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "script.sh"), "w")).close()
        plugins = discover_plugins()
        assert plugins == []

    def test_plugin_action_is_callable(self, tmp_config_dir):
        os.makedirs(C.CUSTOM_TOOLS_DIR, exist_ok=True)
        (open(os.path.join(C.CUSTOM_TOOLS_DIR, "tool.py"), "w")).close()
        plugins = discover_plugins()
        assert callable(plugins[0][2])
