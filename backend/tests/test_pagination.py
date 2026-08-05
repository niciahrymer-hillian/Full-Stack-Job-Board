"""Tests for the pure pagination helper — runnable with just pytest, no DB."""
import pytest

from app.pagination import MAX_PAGE_SIZE, paginate


def test_first_page_has_zero_offset():
    assert paginate(page=1, size=20) == (0, 20)


def test_offset_advances_by_page():
    assert paginate(page=3, size=20) == (40, 20)


def test_page_below_one_clamps_to_first_page():
    assert paginate(page=0, size=20) == (0, 20)
    assert paginate(page=-5, size=20) == (0, 20)


def test_size_is_capped_at_max():
    offset, limit = paginate(page=1, size=10_000)
    assert limit == MAX_PAGE_SIZE


def test_size_below_one_clamps_to_one():
    assert paginate(page=1, size=0) == (0, 1)
