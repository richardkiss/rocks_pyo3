import rocks_pyo3
import tempfile
import pytest


def test_invalid_db_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(Exception):
            rocks_pyo3.DB("/invalid/path/that/does/not/exist", create_if_missing=False)


def test_empty_key_handling():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        db.put(b"", b"empty key")  # Should not raise
        assert db.get(b"") == b"empty key"
