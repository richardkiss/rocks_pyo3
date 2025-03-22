import rocks_pyo3
import tempfile
import pytest

def test_invalid_db_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(Exception):
            rocks_pyo3.DB("/invalid/path/that/does/not/exist")

def test_empty_key_handling():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir)
        with pytest.raises(Exception):
            db.put(b"", b"empty key")
