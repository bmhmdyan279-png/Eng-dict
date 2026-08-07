"""تست‌های واحد برای build_pages.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
from build_pages import normalize_persian, slugify_fa, get_first_letter_normalized

class TestNormalizePersian:
    def test_ye_arabic_to_persian(self):
        assert normalize_persian("كتاب") == "کتاب"

    def test_kaf_arabic_to_persian(self):
        assert normalize_persian("كتاب") == "کتاب"  # كاف عربی به کاف فارسی

    def test_mixed(self):
        assert normalize_persian("يكي دو سه") == "یکی دو سه"

    def test_empty_string(self):
        assert normalize_persian("") == ""

class TestSlugifyFa:
    def test_simple(self):
        result = slugify_fa("سلام دنیا")
        assert "-" in result
        assert len(result) > 0

    def test_special_chars(self):
        result = slugify_fa("آب و خاک!")
        assert "!" not in result
        assert len(result) > 0

    def test_empty(self):
        result = slugify_fa("")
        assert result == ""

class TestGetFirstLetterNormalized:
    def test_normal_letter(self):
        assert get_first_letter_normalized("بتن") == "ب"

    def test_arabic_ye(self):
        assert get_first_letter_normalized("ياس") == "ی"

    def test_empty(self):
        assert get_first_letter_normalized("") == "#"

    def test_none_like(self):
        assert get_first_letter_normalized("   ") == "#"