"""Tests for BND.lib.ui — UI component builders."""
import colorsys

import pytest
from rich.panel import Panel
from rich.text import Text

from BND.lib.ui import make_card_cell, make_title_text, monitor_block


class TestMakeTitleText:
    def test_returns_text(self):
        result = make_title_text("BND-TOOLS")
        assert isinstance(result, Text)

    def test_default_phase_cyan(self):
        result = make_title_text("BND-TOOLS", phase=0)
        assert isinstance(result, Text)

    def test_rainbow_phase(self):
        result = make_title_text("BND-TOOLS", phase=0.5)
        assert isinstance(result, Text)

    def test_title_in_text(self):
        result = make_title_text("TestTitle")
        assert "TestTitle" in result.plain


class TestMakeCardCell:
    def test_returns_panel(self):
        result = make_card_cell("01", "IP Lookup")
        assert isinstance(result, Panel)

    def test_selected_card(self):
        result = make_card_cell("01", "IP Lookup", is_selected=True)
        assert isinstance(result, Panel)

    def test_unselected_card(self):
        result = make_card_cell("01", "IP Lookup", is_selected=False)
        assert isinstance(result, Panel)

    def test_rainbow_card(self):
        result = make_card_cell("01", "IP Lookup", phase=0.5)
        assert isinstance(result, Panel)

    def test_selected_rainbow_card(self):
        result = make_card_cell("01", "IP Lookup", is_selected=True, phase=0.5)
        assert isinstance(result, Panel)


class TestMonitorBlock:
    def test_returns_panel(self, tmp_config_dir, reset_settings):
        result = monitor_block(
            cat_label="OSINT",
            n_tools=5,
            tools=[("01", "A", None), ("02", "B", None)],
            username="TestUser",
            nuker_status=(False, False),
            badge="",
        )
        assert isinstance(result, Panel)

    def test_with_nuker_active(self, tmp_config_dir, reset_settings):
        result = monitor_block(
            cat_label="OSINT",
            n_tools=3,
            tools=[],
            username="TestUser",
            nuker_status=(True, True),
            badge="",
        )
        assert isinstance(result, Panel)

    def test_with_badge(self, tmp_config_dir, reset_settings):
        result = monitor_block(
            cat_label="OSINT",
            n_tools=1,
            tools=[],
            username="TestUser",
            nuker_status=(False, False),
            badge="NEW",
        )
        assert isinstance(result, Panel)

    def test_with_rainbow_phase(self, tmp_config_dir, reset_settings):
        result = monitor_block(
            cat_label="OSINT",
            n_tools=1,
            tools=[],
            username="TestUser",
            nuker_status=(False, False),
            badge="",
            phase=0.5,
        )
        assert isinstance(result, Panel)
