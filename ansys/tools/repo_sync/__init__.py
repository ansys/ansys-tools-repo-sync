"""Tool to synchronize the content of different repositories."""
try:
    import importlib.metadata as importlib_metadata
except PackageNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__package__ or __name__)
from .repo_sync import synchronize
