"""Tests for BND.lib.void_common — UI helpers and pure utility functions."""
import pytest

from BND.lib.void_common import (
    ansi_hex,
    append_star_unlock_items,
    count_free_premium,
    fmt_label,
    is_premium,
    is_star_unlock,
    sort_free_first,
    tw,
    th,
)


class TestAnsiHex:
    def test_basic_hex(self):
        result = ansi_hex("#FF0000")
        assert result == "\033[38;2;255;0;0m"

    def test_hex_without_hash(self):
        result = ansi_hex("00FF00")
        assert result == "\033[38;2;0;255;0m"

    def test_blue_hex(self):
        result = ansi_hex("#0000FF")
        assert result == "\033[38;2;0;0;255m"

    def test_white_hex(self):
        result = ansi_hex("#FFFFFF")
        assert result == "\033[38;2;255;255;255m"

    def test_black_hex(self):
        result = ansi_hex("#000000")
        assert result == "\033[38;2;0;0;0m"

    def test_arbitrary_color(self):
        result = ansi_hex("#C0C0C0")
        assert result == "\033[38;2;192;192;192m"


class TestFmtLabel:
    def test_simple_label(self):
        assert fmt_label("IP Lookup") == "IP Lookup"

    def test_strips_premium_tag(self):
        assert fmt_label("RAR Cracker [PREMIUM]") == "RAR Cracker"

    def test_strips_star_tag(self):
        assert fmt_label("Star for unlock [STAR]") == "Star for unlock"

    def test_case_insensitive_strip(self):
        assert fmt_label("Tool [premium]") == "Tool"

    def test_truncates_long_label(self):
        long_label = "A" * 30
        result = fmt_label(long_label, max_len=24)
        assert len(result) == 24
        assert result.endswith("…")

    def test_truncates_at_custom_length(self):
        result = fmt_label("A" * 15, max_len=10)
        assert len(result) == 10
        assert result.endswith("…")

    def test_no_truncation_when_short(self):
        assert fmt_label("Short", max_len=24) == "Short"

    def test_strips_then_truncates(self):
        label = "A" * 30 + " [PREMIUM]"
        result = fmt_label(label, max_len=24)
        assert len(result) == 24
        assert "[PREMIUM]" not in result


class TestIsPremium:
    def test_premium_label(self):
        assert is_premium("RAR Cracker [PREMIUM]") is True

    def test_star_label_is_premium(self):
        assert is_premium("Star for unlock [STAR]") is True

    def test_free_label(self):
        assert is_premium("IP Lookup") is False

    def test_empty_string(self):
        assert is_premium("") is False

    def test_case_insensitive(self):
        assert is_premium("Tool [premium]") is True

    def test_partial_match_no(self):
        assert is_premium("PREMIUM tool") is False


class TestIsStarUnlock:
    def test_star_label(self):
        assert is_star_unlock("Star for unlock [STAR]") is True

    def test_non_star_label(self):
        assert is_star_unlock("IP Lookup") is False

    def test_case_insensitive(self):
        assert is_star_unlock("Tool [star]") is True

    def test_premium_is_not_star(self):
        assert is_star_unlock("Tool [PREMIUM]") is False


class TestSortFreeFirst:
    def _make_items(self, labels):
        return [(f"{i+1:02d}", label, lambda: None) for i, label in enumerate(labels)]

    def test_empty_list(self):
        assert sort_free_first([]) == []

    def test_none_returns_none(self):
        assert sort_free_first(None) is None

    def test_free_before_premium(self):
        items = self._make_items(["Free A", "Paid [PREMIUM]", "Free B"])
        result = sort_free_first(items)
        labels = [r[1] for r in result]
        free_indices = [i for i, l in enumerate(labels) if "[PREMIUM]" not in l]
        prem_indices = [i for i, l in enumerate(labels) if "[PREMIUM]" in l]
        if prem_indices and free_indices:
            assert max(free_indices) < min(prem_indices)

    def test_renumbering(self):
        items = self._make_items(["B", "A"])
        result = sort_free_first(items)
        codes = [r[0] for r in result]
        assert codes == ["01", "02"]

    def test_head_code_00_stays_first(self):
        items = [("00", "Home", lambda: None), ("01", "Tool A", lambda: None)]
        result = sort_free_first(items)
        assert result[0][0] == "00"

    def test_tail_code_x_stays_last(self):
        items = [
            ("01", "Tool A", lambda: None),
            ("X", "Exit", lambda: None),
            ("02", "Tool B", lambda: None),
        ]
        result = sort_free_first(items)
        assert result[-1][1] == "Exit"

    def test_all_free(self):
        items = self._make_items(["A", "B", "C"])
        result = sort_free_first(items)
        assert len(result) == 3

    def test_all_premium(self):
        items = self._make_items(["A [PREMIUM]", "B [PREMIUM]"])
        result = sort_free_first(items)
        assert len(result) == 2


class TestCountFreePremium:
    def test_empty(self):
        assert count_free_premium([]) == (0, 0)

    def test_all_free(self):
        items = [("01", "Tool A", None), ("02", "Tool B", None)]
        assert count_free_premium(items) == (2, 0)

    def test_all_premium(self):
        items = [("01", "A [PREMIUM]", None), ("02", "B [PREMIUM]", None)]
        assert count_free_premium(items) == (0, 2)

    def test_mixed(self):
        items = [
            ("01", "Free Tool", None),
            ("02", "Paid [PREMIUM]", None),
            ("03", "Star [STAR]", None),
        ]
        assert count_free_premium(items) == (1, 2)


class TestAppendStarUnlockItems:
    def test_empty_list(self):
        assert append_star_unlock_items([]) == []

    def test_none_returns_none(self):
        assert append_star_unlock_items(None) is None

    def test_appends_four_items(self, tmp_config_dir, reset_settings):
        items = [("01", "Tool A", lambda: None)]
        result = append_star_unlock_items(items)
        assert len(result) == 5  # 1 original + 4 star unlock
        for added in result[1:]:
            assert "[STAR]" in added[1]

    def test_star_items_have_correct_codes(self, tmp_config_dir, reset_settings):
        items = [("01", "A", lambda: None), ("02", "B", lambda: None)]
        result = append_star_unlock_items(items)
        star_codes = [r[0] for r in result[2:]]
        assert star_codes == ["03", "04", "05", "06"]


class TestTerminalSize:
    def test_tw_returns_int(self):
        assert isinstance(tw(), int)
        assert tw() > 0

    def test_th_returns_int(self):
        assert isinstance(th(), int)
        assert th() > 0
