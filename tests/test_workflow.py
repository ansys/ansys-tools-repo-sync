import os
import sys
import io
import shutil
import subprocess
import tempfile
import time

import github
from github.GithubException import UnknownObjectException

from ansys.tools.repo_sync import synchronize


THIS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIRECTORY = os.path.join(THIS_PATH, "assets")
TOKEN = os.environ["TOKEN"]


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
                token=TOKEN,
                repository="ansys-tools-repo-sync",
                organization="ansys",
                protos_path=os.path.join("assets", "ansys", "api", "test", "v0"),
                dry_run=False,
            )

    gh = github.Github(TOKEN)
    repo = gh.get_repo("ansys/ansys-tools-repo-sync")

    for pull_request in repo.get_pulls():
        if pull_request.title == "Add folder content from assets/ansys/api/test/v0.":
            time.sleep(50)
            pull_request.edit(state="closed")
            # Following assertion is required to be sure that the PR was created
            # and deleted properly. Otherwise, there is no way to make sure that it
            # worked properly as it is deleted automatically.
            assert True
            break

    branch_name = "sync/sync_branch"
    try:
        ref = repo.get_git_ref(branch_name)
        ref.delete()
    except UnknownObjectException:
        print("No such branch", branch_name)

    assert "Synchronization Succeeded..." in str(capture.content)


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
                token=TOKEN,
                repository="ansys-tools-repo-sync",
                organization="ansys",
                protos_path=os.path.join("assets", "ansys", "api", "test", "v0"),
                dry_run=True,
            )

    assert "Dry-run synchronization output:" in str(capture.content)
