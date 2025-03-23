import rocks_pyo3
import tempfile


def test_basic_crud():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)

        # Test put and get
        db.put(b"test_key", b"test_value")
        assert db.get(b"test_key") == b"test_value"

        # Test delete
        db.delete(b"test_key")
        assert db.get(b"test_key") is None


def test_multi_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)

        data = {b"key1": b"val1", b"key2": b"val2", b"key3": b"val3"}

        for k, v in data.items():
            db.put(k, v)

        # Test valid and invalid keys
        results = db.multi_get([b"key1", b"key2", b"missing"])
        assert results[0] == b"val1"
        assert results[1] == b"val2"
        assert results[2] is None
