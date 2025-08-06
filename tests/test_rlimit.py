import sys
import pytest

from rocks_pyo3.rlimit import maximize_nofile_limit


def test_maximize_nofile_limit_sets_soft_to_hard():
    """Test maximize_nofile_limit behavior on all platforms."""
    result = maximize_nofile_limit()
    if sys.platform == "win32":
        assert result is None
    else:
        assert isinstance(result, tuple)
        assert len(result) == 2
        soft, hard = result
        assert soft == hard
        assert soft > 0
        assert hard > 0


def test_maximize_nofile_limit_idempotent():
    """Test that calling maximize_nofile_limit twice is idempotent or always returns None on Windows."""
    first = maximize_nofile_limit()
    second = maximize_nofile_limit()
    if sys.platform == "win32":
        assert first is None
        assert second is None
    else:
        assert first == second
        soft, hard = first
        assert soft == hard


def test_maximize_nofile_limit_unsupported(monkeypatch):
    """Test that maximize_nofile_limit returns None if resource module is unavailable."""
    import rocks_pyo3.rlimit as rlimit_mod

    monkeypatch.setattr(rlimit_mod, "resource", None)
    monkeypatch.setattr(rlimit_mod, "RLIMIT_NOFILE", None)
    result = rlimit_mod.maximize_nofile_limit()
    assert result is None
