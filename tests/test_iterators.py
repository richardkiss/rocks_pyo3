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


def test_reverse_iteration():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)

        data = [(b"a", b"1"), (b"b", b"2"), (b"c", b"3"), (b"d", b"4")]
        for k, v in data:
            db.put(k, v)

        # Verify data is in the DB using forward iterator
        forward_data = list(db.iterator())
        assert forward_data == data, f"Forward data doesn't match: {forward_data}"

        it = db.iterator(direction="reverse")
        result = list(it)
        expected = list(reversed(data))
        assert result == expected, f"Got {result}, expected {expected}"


def test_iterate_from_key_reverse():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)

        data = [(b"a", b"1"), (b"b", b"2"), (b"c", b"3"), (b"d", b"4")]
        for k, v in data:
            db.put(k, v)

        it = db.iterate_from(b"c", direction="reverse")
        assert list(it) == [data[2], data[1], data[0]]


def test_empty_iteration():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = rocks_pyo3.DB(tmpdir, create_if_missing=True)

        db.put(b"a", b"1")
        db.delete(b"a")
        assert len(list(db.iterator())) == 0
