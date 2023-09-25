"""Tool to synchronize the content of different repositories."""

# Version
# ------------------------------------------------------------------------------

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version("ansys-tools-repo-sync")

# Ease import statements
# ------------------------------------------------------------------------------

from .repo_sync import synchronize
