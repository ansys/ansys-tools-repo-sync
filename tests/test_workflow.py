import os
import sys
import io
import shutil
import subprocess
import tempfile

from ansys.tools.repo_sync import synchronize


THIS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIRECTORY = os.path.join(THIS_PATH, "assets")


class CaptureStdOut:
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


def test_synchronization():
    """Test standard synchronization."""

    token = os.environ["TEST_TOKEN"]
    print(token[4:7])

    # Create a temp directory that will be used as a fake public repo
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Add control version to the temp directory
        process = subprocess.Popen(
            ["git", "init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        # copy proto file.
        shutil.copytree(
            os.path.join(ASSETS_DIRECTORY, "ansys", "api", "test", "v0"),
            os.path.join(os.getcwd(), "assets", "ansys", "api", "test", "v0"),
        )

        capture = CaptureStdOut()
        with capture:
            synchronize(
                manifest=os.path.join(ASSETS_DIRECTORY, "manifest.txt"),
                token=None,
                repository="ansys-tools-repo-sync",
                organization="ansys",
                protos_path=r"assets\ansys\api\test\v0",
                dry_run=True,
            )

    assert "Dry-run synchronization output:" in str(capture.content)
    assert "On branch sync/sync_branch" in str(capture.content)
    assert "Changes to be committed:" in str(capture.content)
    assert "new file:   assets/ansys/api/test/v0/test.proto" in str(capture.content)


def test_dry_run():
    """Test dry-run option."""

    # Create a temp directory that will be used as a fake public repo
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)

        # Add control version to the temp directory
        process = subprocess.Popen(
            ["git", "init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        # copy proto file.
        shutil.copytree(
            os.path.join(ASSETS_DIRECTORY, "ansys", "api", "test", "v0"),
            os.path.join(os.getcwd(), "assets", "ansys", "api", "test", "v0"),
        )

        capture = CaptureStdOut()
        with capture:
            synchronize(
                manifest=os.path.join(ASSETS_DIRECTORY, "manifest.txt"),
                token=None,
                repository="ansys-tools-repo-sync",
                organization="ansys",
                protos_path=r"assets\ansys\api\test\v0",
                dry_run=True,
            )

    assert "Dry-run synchronization output:" in str(capture.content)


# test_002()
