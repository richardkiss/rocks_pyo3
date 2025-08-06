from .rocks_pyo3 import DB, WriteBatch
from .rlimit import possibly_maximize_nofile_limit

__all__ = ["DB", "WriteBatch"]


# Automatically attempt to maximize RLIMIT_NOFILE on import
# set the environment variable ROCKS_PYO3_SKIP_RLIMIT to skip this behavior
possibly_maximize_nofile_limit()
