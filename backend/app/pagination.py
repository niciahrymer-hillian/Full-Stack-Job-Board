"""Pure pagination helper — no FastAPI, no DB, so it's trivially unit-testable.

Keeping the math here (instead of inline in the router) is the lesson: pure
functions are the easiest thing in the codebase to test and the first thing to
get right. See tests/test_pagination.py.
"""

MAX_PAGE_SIZE = 100


def paginate(page: int = 1, size: int = 20) -> tuple[int, int]:
    """Return (offset, limit) for a 1-based page number.

    Page numbers below 1 clamp to 1; sizes are clamped to [1, MAX_PAGE_SIZE] so a
    client can never request an unbounded result set.
    """
    page = max(1, page)
    size = max(1, min(size, MAX_PAGE_SIZE))
    return (page - 1) * size, size
