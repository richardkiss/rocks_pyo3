"""
Utility to increase the RLIMIT_NOFILE soft limit to the hard limit for the current process.

Usage example:
    from rocks_pyo3.rlimit import maximize_nofile_limit

    new_soft, new_hard = maximize_nofile_limit()
    print(f"Soft limit: {new_soft}, Hard limit: {new_hard}")

Platform: Unix-like systems only (uses the 'resource' module).
"""

from typing import Optional, Tuple

try:
    import resource

    RLIMIT_NOFILE = resource.RLIMIT_NOFILE
except ImportError:
    resource = None


def maximize_nofile_limit() -> Optional[Tuple[int, int]]:
    """
    Increase the RLIMIT_NOFILE soft limit to the hard limit for the current process.

    Returns
    -------
    (soft, hard) : tuple of int
        The new soft and hard limits for open file descriptors.
    """
    if resource is None:
        return None

    soft, hard = resource.getrlimit(RLIMIT_NOFILE)
    if soft < hard:
        try:
            resource.setrlimit(RLIMIT_NOFILE, (hard, hard))
            soft = hard
        except (ValueError, resource.error) as e:
            raise RuntimeError(f"Failed to maximize RLIMIT_NOFILE: {e}")
    return soft, hard


def possibly_maximize_nofile_limit() -> Optional[Tuple[int, int]]:
    """
    Escape hatch for automatic RLIMIT_NOFILE maximization.

    On import, this function will attempt to maximize RLIMIT_NOFILE automatically,
    unless the environment variable `ROCKS_PYO3_SKIP_RLIMIT` is set.

    Returns
    -------
    (soft, hard) : tuple of int, or None
        The new soft and hard limits for open file descriptors, or None if skipped or unsupported.

    Escape hatch:
        To prevent automatic RLIMIT_NOFILE adjustment on import, set the environment variable
        `ROCKS_PYO3_SKIP_RLIMIT` to any value before running your Python process.

    Usage example:
        from rocks_pyo3.rlimit import maximize_nofile_limit

        new_soft, new_hard = maximize_nofile_limit()
        print(f"Soft limit: {new_soft}, Hard limit: {new_hard}")
    """
    import os

    if os.environ.get("ROCKS_PYO3_SKIP_RLIMIT"):
        return None
    return maximize_nofile_limit()
