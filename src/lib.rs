use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use rocksdb::{Direction, IteratorMode, Options, DB};
use std::path::Path;

#[pyclass(name = "DB")]
struct PyDB {
    db: DB,
}

#[pymethods]
impl PyDB {
    #[new]
    #[pyo3(signature = (path, create_if_missing=None))]
    fn new(path: &str, create_if_missing: Option<bool>) -> PyResult<Self> {
        let mut opts = Options::default();
        opts.create_if_missing(create_if_missing.unwrap_or(true));

        DB::open(&opts, Path::new(path))
            .map(|db| PyDB { db })
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    fn put(&self, key: &[u8], value: &[u8]) -> PyResult<()> {
        self.db
            .put(key, value)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    fn get(&self, py: Python<'_>, key: &[u8]) -> PyResult<Option<Py<PyBytes>>> {
        self.db
            .get(key)
            .map(|value| value.map(|v| PyBytes::new(py, &v).into()))
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    fn multi_get(&self, py: Python<'_>, keys: Vec<Vec<u8>>) -> PyResult<Vec<Option<Py<PyBytes>>>> {
        let values = self.db.multi_get(&keys);
        let mut r: Vec<Option<Py<PyBytes>>> = Vec::with_capacity(values.len());
        for value in values {
            if let Err(e) = value {
                return Err(PyRuntimeError::new_err(e.to_string()));
            }
            if let Ok(Some(value)) = value {
                r.push(Some(PyBytes::new(py, &value).into()));
            } else {
                r.push(None);
            }
        }
        Ok(r)
    }

    fn delete(&self, key: &[u8]) -> PyResult<()> {
        self.db
            .delete(key)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }

    #[pyo3(signature = (direction = "forward"))]
    fn iterator(slf: Py<Self>, py: Python, direction: &str) -> PyResult<Py<DBIterator>> {
        let dir = match direction.to_lowercase().as_str() {
            "forward" => Direction::Forward,
            "reverse" => Direction::Reverse,
            _ => {
                return Err(PyValueError::new_err(
                    "Invalid direction, must be 'forward' or 'reverse'",
                ))
            }
        };
        // we need to bump the reference count to the db so that it lives as
        // long as the iterator
        let db: Py<PyDB> = slf.clone_ref(py);
        let bound_db = db.bind(py);
        let db_ref = bound_db.borrow();

        // Use the appropriate iterator mode based on direction
        let iter = match dir {
            Direction::Forward => db_ref.db.iterator(IteratorMode::Start),
            Direction::Reverse => db_ref.db.iterator(IteratorMode::End),
        };

        let iter: rocksdb::DBIterator<'static> = unsafe { std::mem::transmute(iter) }; // erase the lifetime
        Py::new(py, DBIterator { iter, _db: db })
    }

    #[pyo3(signature = (key, direction = "forward"))]
    fn iterate_from(
        slf: Py<Self>,
        py: Python,
        key: &[u8],
        direction: &str,
    ) -> PyResult<Py<DBIterator>> {
        let dir = match direction.to_lowercase().as_str() {
            "forward" => Direction::Forward,
            "reverse" => Direction::Reverse,
            _ => {
                return Err(PyValueError::new_err(
                    "Invalid direction, must be 'forward' or 'reverse'",
                ))
            }
        };
        let db: Py<PyDB> = slf.clone_ref(py);
        let bound_db = db.bind(py);
        let db_ref = bound_db.borrow();
        let iter = db_ref.db.iterator(IteratorMode::From(key, dir));
        let iter: rocksdb::DBIterator<'static> = unsafe { std::mem::transmute(iter) };
        Py::new(py, DBIterator { iter, _db: db })
    }

    fn write(&self, batch: &mut PyWriteBatch) -> PyResult<()> {
        batch.write(self)
    }

    fn approximate_size(&self) -> PyResult<u64> {
        // Get property for approximate size
        match self.db.property_int_value("rocksdb.estimate-num-keys") {
            Ok(Some(size)) => Ok(size),
            Ok(None) => Ok(0),
            Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
        }
    }

    // Convenience method for putting string key/value pairs
    fn put_str(&self, key: &str, value: &str) -> PyResult<()> {
        self.put(key.as_bytes(), value.as_bytes())
    }
}

#[pyclass]
pub struct DBIterator {
    iter: rocksdb::DBIterator<'static>,
    // we store `db` but never use it to ensure it lives as long as the iterator
    _db: Py<PyDB>,
}

#[pymethods]
impl DBIterator {
    fn __iter__(slf: Py<Self>) -> Py<DBIterator> {
        slf
    }
    fn __next__(&mut self, py: Python) -> PyResult<Option<(PyObject, PyObject)>> {
        if let Some(result) = self.iter.next() {
            match result {
                Ok((key, value)) => {
                    let py_key = PyBytes::new(py, &key).into();
                    let py_value = PyBytes::new(py, &value).into();
                    Ok(Some((py_key, py_value)))
                }
                Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
            }
        } else {
            Ok(None)
        }
    }
}

#[pyclass(name = "WriteBatch", unsendable)]
struct PyWriteBatch {
    batch: Option<rocksdb::WriteBatch>,
}

#[pymethods]
impl PyWriteBatch {
    #[new]
    fn new() -> Self {
        PyWriteBatch {
            batch: Some(rocksdb::WriteBatch::default()),
        }
    }

    fn put(&mut self, key: &[u8], value: &[u8]) -> PyResult<()> {
        match &mut self.batch {
            Some(batch) => {
                batch.put(key, value);
                Ok(())
            }
            None => Err(PyRuntimeError::new_err("WriteBatch has already been used")),
        }
    }

    fn delete(&mut self, key: &[u8]) -> PyResult<()> {
        match &mut self.batch {
            Some(batch) => {
                batch.delete(key);
                Ok(())
            }
            None => Err(PyRuntimeError::new_err("WriteBatch has already been used")),
        }
    }

    fn write(&mut self, db: &PyDB) -> PyResult<()> {
        // Take ownership of the batch, replacing it with None
        let write_batch = match self.batch.take() {
            Some(batch) => batch,
            None => return Err(PyRuntimeError::new_err("WriteBatch has already been used")),
        };

        // Write the batch directly to the database
        db.db
            .write(write_batch)
            .map_err(|e| PyRuntimeError::new_err(e.to_string()))
    }
}

#[pymodule]
fn rocks_pyo3(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyDB>()?;
    m.add_class::<DBIterator>()?;
    m.add_class::<PyWriteBatch>()?;
    Ok(())
}
