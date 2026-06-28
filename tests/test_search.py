"""Tests for BND.lib.search — fuzzy search, filters, scoring."""
import pytest

from BND.lib.search import _score, parse_filters, search_tools


class TestParseFilters:
    def test_no_filters(self):
        tier, cat, q = parse_filters("ip lookup")
        assert tier is None
        assert cat is None
        assert q == "ip lookup"

    def test_free_filter(self):
        tier, cat, q = parse_filters("free: ip lookup")
        assert tier == "free"
        assert q == "ip lookup"

    def test_free_without_colon(self):
        tier, cat, q = parse_filters("free ip lookup")
        assert tier == "free"
        assert q == "ip lookup"

    def test_premium_filter(self):
        tier, cat, q = parse_filters("prem: cracker")
        assert tier == "premium"

    def test_premium_full_word(self):
        tier, cat, q = parse_filters("premium cracker")
        assert tier == "premium"

    def test_category_filter(self):
        tier, cat, q = parse_filters("cat:discord token")
        assert cat == "discord"
        assert q == "token"

    def test_combined_filters(self):
        tier, cat, q = parse_filters("free: cat:osint lookup")
        assert tier == "free"
        assert cat == "osint"
        assert q == "lookup"

    def test_empty_string(self):
        tier, cat, q = parse_filters("")
        assert tier is None
        assert cat is None
        assert q == ""

    def test_only_free_filter(self):
        tier, cat, q = parse_filters("free:")
        assert tier == "free"
        assert q == "free:"

    def test_category_case_preserved(self):
        tier, cat, q = parse_filters("cat:Discord")
        assert cat == "discord"

    def test_whitespace_handling(self):
        tier, cat, q = parse_filters("  ip  lookup  ")
        assert q == "ip lookup"


class TestScore:
    def test_exact_match_in_label(self):
        score = _score("ip lookup", "IP Lookup", "OSINT", "01")
        assert score > 1.0

    def test_partial_match(self):
        score = _score("lookup", "IP Lookup Tool", "OSINT", "01")
        assert score > 1.0

    def test_no_match(self):
        score = _score("xyznotfound", "IP Lookup", "OSINT", "01")
        assert score < 0.5

    def test_token_match(self):
        score = _score("ip tool", "IP Lookup Tool", "Network", "05")
        assert score >= 0.85

    def test_category_match(self):
        score = _score("osint", "IP Scanner", "OSINT Tools", "02")
        assert score > 1.0

    def test_code_match(self):
        score = _score("05", "Any Tool", "Category", "05")
        assert score >= 1.0

    def test_fuzzy_similarity(self):
        score = _score("loookup", "IP Lookup", "OSINT", "01")
        assert score > 0  # fuzzy match should give some score

    def test_case_insensitive(self):
        s1 = _score("IP LOOKUP", "ip lookup", "osint", "01")
        s2 = _score("ip lookup", "IP LOOKUP", "OSINT", "01")
        assert s1 == s2

    def test_exact_scores_higher_than_fuzzy(self):
        exact = _score("ip lookup", "IP Lookup", "OSINT", "01")
        fuzzy = _score("ip loookup", "IP Lookup", "OSINT", "01")
        assert exact > fuzzy


class TestSearchTools:
    @pytest.fixture()
    def sample_data(self):
        categories = [
            ("osint", "OSINT"),
            ("network", "Network"),
        ]
        pages_data = {
            "osint": [
                ("01", "IP Lookup", lambda: None),
                ("02", "Email OSINT", lambda: None),
                ("03", "Premium Scanner [PREMIUM]", lambda: None),
            ],
            "network": [
                ("01", "Port Scanner", lambda: None),
                ("02", "DNS Lookup", lambda: None),
            ],
        }
        return categories, pages_data

    def test_empty_query_no_filters(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "")
        assert results == []

    def test_basic_search(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "lookup")
        assert len(results) >= 2
        labels = [r[3] for r in results]
        assert "IP Lookup" in labels
        assert "DNS Lookup" in labels

    def test_search_returns_tuples(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "lookup")
        for r in results:
            assert len(r) == 5  # (score, cat_label, code, label, action)

    def test_results_sorted_by_score(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "ip")
        if len(results) >= 2:
            scores = [r[0] for r in results]
            assert scores == sorted(scores, reverse=True)

    def test_free_filter(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "free: scanner")
        labels = [r[3] for r in results]
        assert "Premium Scanner [PREMIUM]" not in labels

    def test_premium_filter(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "prem:")
        for r in results:
            assert "[PREMIUM]" in r[3]

    def test_category_filter(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "cat:network")
        for r in results:
            assert r[1] == "Network"

    def test_limit(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "a", limit=2)
        assert len(results) <= 2

    def test_no_results(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "xyznonexistent123")
        assert results == []

    def test_category_filter_case_insensitive(self, sample_data):
        cats, pages = sample_data
        results = search_tools(cats, pages, "cat:OSINT")
        for r in results:
            assert r[1] == "OSINT"
