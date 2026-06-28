"""Tests for BND.lib.deps — dependency checking."""
import pytest

from BND.lib.deps import OPTIONAL, REQUIRED, check_deps


class TestDependencyLists:
    def test_required_has_colorama(self):
        mods = [m for m, _ in REQUIRED]
        assert "colorama" in mods

    def test_required_has_rich(self):
        mods = [m for m, _ in REQUIRED]
        assert "rich" in mods

    def test_optional_has_requests(self):
        pkgs = [p for _, p in OPTIONAL]
        assert "requests" in pkgs

    def test_optional_has_dnspython(self):
        pkgs = [p for _, p in OPTIONAL]
        assert "dnspython" in pkgs

    def test_required_format(self):
        for mod, pkg in REQUIRED:
            assert isinstance(mod, str)
            assert isinstance(pkg, str)


class TestCheckDeps:
    def test_returns_bool(self):
        result = check_deps(auto_install=False)
        assert isinstance(result, bool)

    def test_required_deps_installed(self):
        # colorama may not be installed; check_deps returns True when
        # no *required* packages are missing (optional ones are OK to miss)
        import importlib
        missing_required = []
        for mod, pkg in REQUIRED:
            try:
                importlib.import_module(mod)
            except ImportError:
                missing_required.append(pkg)
        result = check_deps(auto_install=False)
        if not missing_required:
            assert result is True
        else:
            assert result is False
