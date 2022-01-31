import os
import sys
import io
import subprocess
import tempfile

import pytest

from ansys.tools.repo_sync import synchronize


THIS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIRECTORY = os.path.join(THIS_PATH, 'assets')


class CaptureStdOut():
    """Capture standard output with a context manager."""

    def __init__(self):
        self._stream = io.StringIO()

    def __enter__(self):
        sys.stdout = self._stream

    def __exit__(self, type, value, traceback):
        sys.stdout = sys.__stdout__

    @property
    def content(self):
        """Return the captured content."""
        return self._stream.getvalue()


def test_001():
    """ Test."""

    # Create a temp directory that will be used as a fake public repo

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Add control version to the temp directory
        process = subprocess.Popen(
            ["git", "init", "--bare", "test_repo.git"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()



    capture = CaptureStdOut()
    with capture:
        synchronize(
            manifest=os.path.join(ASSETS_DIRECTORY, "manifest.txt"),
            token=None,
            repository="ansys-tools-repo-sync",
            organization="ansys",
            protos_path=r"D:\GitHub\ansys-tools-repo-sync\tests\assets\ansys\api\test\v0",
            dry_run=True)

    assert "No python modules found in:" in str(capture.content)
