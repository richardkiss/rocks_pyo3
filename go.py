import rocks_pyo3
import tempfile
import pytest

def test_basic_crud():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        # Test put and get
        db.put(b"test_key", b"test_value")
        assert db.get(b"test_key")[0] == b"test_value"
        
        # Test delete
        db.delete(b"test_key")
        assert db.get(b"test_key")[0] is None

def test_multi_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        data = {
            b"key1": b"val1",
            b"key2": b"val2",
            b"key3": b"val3"
        }
        
        for k, v in data.items():
            db.put(k, v)
            
        # Test valid and invalid keys
        results = db.multi_get([b"key1", b"key2", b"missing"])
        assert results[0][0] == b"val1"
        assert results[1][0] == b"val2"
        assert results[2][0] is None

def test_iterators():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        # Insert test data in sorted order
        data = [(b"a", b"1"), (b"b", b"2"), (b"c", b"3"), (b"d", b"4")]
        for k, v in data:
            db.put(k, v)
            
        # Test forward iteration
        it = db.iterator()
        assert list(it) == data
        
        # Test iteration from middle
        it = db.iterate_from(b"b")
        assert list(it) == data[1:]
        
        # Test empty iterator
        db.delete(b"a")
        db.delete(b"b")
        db.delete(b"c")
        db.delete(b"d")
        assert len(list(db.iterator())) == 0

def test_error_handling():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test invalid path
        with pytest.raises(Exception):
            rocks_pyo3.DB("/invalid/path/that/does/not/exist")
            
        # Test valid creation
        db = rocks_pyo3.DB(tmpdir)
        with pytest.raises(Exception):
            db.put(b"", b"empty key")

if __name__ == "__main__":
    pytest.main(["-v", __file__])
