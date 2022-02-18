"""Tool to synchronize the content of different repositories."""
import importlib.metadata
__version__ = importlib.metadata.version(__name__.replace(".", "-"))
from .repo_sync import synchronize
