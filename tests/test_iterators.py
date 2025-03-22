import rocks_pyo3
import tempfile

def test_forward_iteration():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        data = [(b"a", b"1"), (b"b", b"2"), (b"c", b"3"), (b"d", b"4")]
        for k, v in data:
            db.put(k, v)
            
        it = db.iterator()
        assert list(it) == data

def test_iterate_from_key():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        data = [(b"a", b"1"), (b"b", b"2"), (b"c", b"3"), (b"d", b"4")]
        for k, v in data:
            db.put(k, v)

        it = db.iterate_from(b"b")
        assert list(it) == data[1:]

def test_empty_iteration():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)
        
        db.put(b"a", b"1")
        db.delete(b"a")
        assert len(list(db.iterator())) == 0
