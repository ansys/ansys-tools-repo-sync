"""Tool to synchronize the content of different repositories."""
try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = "0.1.dev0"
from .repo_sync import synchronize
