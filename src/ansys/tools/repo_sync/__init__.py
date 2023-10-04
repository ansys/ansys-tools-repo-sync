"""Tool to synchronize the content of different repositories."""

# Version
# ------------------------------------------------------------------------------
import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version("ansys-tools-repo-sync")

# Ease import statements
# ------------------------------------------------------------------------------

from .repo_sync import synchronize
