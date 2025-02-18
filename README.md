# rocks_pyo3: A Python Binding for RocksDB

rocks_pyo3 is a Python library that provides bindings for RocksDB, a high-performance embedded database for key-value data. This library is built using Rust and PyO3, ensuring both speed and safety.

## Features

- **Put**: Insert key-value pairs into the database.
- **Get**: Retrieve values by their keys.
- **Delete**: Remove key-value pairs.
- **Iterator**: Iterate over the database entries.

## Installation

To install rocks_pyo3, use pip:

```bash
pip install rocks_pyo3
```

## Requirements

- Python 3.7 or later
- Rust toolchain
- Clang (required for building `librocksdb-sys`)

## Usage

Here's a quick example of how to use rocks_pyo3:

```python
from rocks_pyo3 import PyDB

# Open or create a database
db = PyDB("example.db")

# Insert a key-value pair
db.put(b"key", b"value")

# Retrieve the value
value = db.get(b"key")
print(value)  # Output: b'value'

# Delete the key-value pair
db.delete(b"key")
```

## Building from Source

To build PyDB from source, ensure you have the following installed:

- Rust toolchain
- Clang
- Python 3.x

Then, run:

```bash
maturin build
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
