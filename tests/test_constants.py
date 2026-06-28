"""Tests for BND.lib.constants — themes, palette, and helpers."""
import colorsys

from BND.lib import constants as C


class TestVersion:
    def test_version_is_string(self):
        assert isinstance(C.VERSION, str)

    def test_version_format(self):
        parts = C.VERSION.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)


class TestPaths:
    def test_void_dir_exists(self):
        assert C.VOID_DIR
        assert isinstance(C.VOID_DIR, str)

    def test_config_dir_under_void(self):
        assert C.CONFIG_DIR.startswith(C.VOID_DIR)

    def test_settings_path_under_config(self):
        assert C.SETTINGS_PATH.startswith(C.CONFIG_DIR)
        assert C.SETTINGS_PATH.endswith("settings.json")

    def test_nuker_cfg_path_under_config(self):
        assert C.NUKER_CFG_PATH.startswith(C.CONFIG_DIR)


class TestThemes:
    def test_default_theme_blue_exists(self):
        assert "blue" in C.THEMES

    def test_blue_theme_has_required_keys(self):
        required = {"blood", "dark", "mid", "red", "neon", "bright"}
        assert required.issubset(C.THEMES["blue"].keys())

    def test_blue_theme_values_are_hex(self):
        for key, val in C.THEMES["blue"].items():
            assert val.startswith("#"), f"Theme value {key}={val} should be hex"

    def test_theme_aliases_contains_blue(self):
        assert "blue" in C._THEME_ALIASES

    def test_apply_theme_valid(self):
        C.apply_theme("blue")
        assert C._ACTIVE_THEME == "blue"

    def test_apply_theme_invalid_no_change(self):
        C.apply_theme("blue")
        C.apply_theme("nonexistent_theme_xyz")
        assert C._ACTIVE_THEME == "blue"

    def test_get_theme_returns_blue(self):
        C.apply_theme("blue")
        theme = C.get_theme()
        assert theme == C.THEMES["blue"]

    def test_get_theme_fallback_to_blue(self):
        original = C._ACTIVE_THEME
        C._ACTIVE_THEME = "missing"
        theme = C.get_theme()
        assert theme == C.THEMES["blue"]
        C._ACTIVE_THEME = original


class TestIsRainbow:
    def test_is_rainbow_returns_false(self):
        assert C.is_rainbow() is False


class TestPalette:
    def test_palette_zero_phase(self):
        pal = C.palette(0)
        assert "primary" in pal
        assert "secondary" in pal
        assert "accent" in pal
        assert "danger" in pal
        assert "success" in pal
        assert "info" in pal

    def test_palette_negative_phase(self):
        pal = C.palette(-1)
        assert pal["primary"] == C.C_BLUE

    def test_palette_positive_phase_rainbow(self):
        pal = C.palette(0.5)
        assert all(key in pal for key in ("primary", "secondary", "accent"))
        # All values should be the same color in rainbow mode
        assert pal["primary"] == pal["secondary"]
        assert pal["primary"] == pal["accent"]

    def test_palette_rainbow_contains_ansi(self):
        pal = C.palette(0.5)
        assert pal["primary"].startswith("\033[38;2;")

    def test_palette_phase_one(self):
        pal = C.palette(1.0)
        r, g, b = colorsys.hsv_to_rgb(1.0, 1.0, 1.0)
        expected = f"\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m"
        assert pal["primary"] == expected


class TestAnsiConstants:
    def test_reset_code(self):
        assert C.C_RESET == "\033[0m"

    def test_bold_code(self):
        assert C.C_BOLD == "\033[1m"

    def test_color_codes_are_ansi(self):
        for name in ("C_RED", "C_GREEN", "C_YELLOW", "C_BLUE", "C_MAGENTA", "C_CYAN", "C_WHITE"):
            val = getattr(C, name)
            assert val.startswith("\033["), f"{name} should be an ANSI code"

    def test_extended_color_codes(self):
        for name in ("C_GOLD", "C_PINK", "C_ORANGE", "C_LIME", "C_TEAL"):
            val = getattr(C, name)
            assert "\033[" in val
