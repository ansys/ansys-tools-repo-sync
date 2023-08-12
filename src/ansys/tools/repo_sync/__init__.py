"""Tool to synchronize the content of different repositories."""

# Version
# ------------------------------------------------------------------------------

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("ansys-tools-repo-sync")

# Ease import statements
# ------------------------------------------------------------------------------

from .repo_sync import synchronize
from .repo_sync_v2 import synchronize_v2
