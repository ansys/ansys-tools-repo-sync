"""Tool to synchronize the content of different repositories."""
__version__ = importlib_metadata.version(__name__.replace(".", "-"))
from .repo_sync import synchronize
