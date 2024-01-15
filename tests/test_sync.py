# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import shutil
import subprocess

import pytest

from ansys.tools.repo_sync.repo_sync import synchronize

from .conftest import (
    ASSETS_DIRECTORY,
    ROOT_PATH,
    SKIP_LOCALLY,
    TOKEN,
    check_files_in_pr,
    cleanup_remote_repo,
    get_pr_from_cli,
)


def test_synchronize():
    """Test synchronization tool (without manifest)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


def test_synchronize_to_existing_pr():
    """Test synchronization tool (when PR already exists)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Call the function again - and check that the PR already exists.
        result_pr_already_exists = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
        )

        # Verify the PR is the same
        assert result_pr_already_exists == result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)
        if result_pr_already_exists and result != result_pr_already_exists:
            cleanup_remote_repo(owner, result_pr_already_exists, result)


def test_synchronize_with_only_proto_manifest():
    """Test synchronization tool (with manifest)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest_only_proto.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


def test_synchronize_no_sync_needed():
    """Test synchronization tool (with manifest referring to non-existing files)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest_no_files.txt")

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            include_manifest=manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert result is None

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)


def test_synchronize_with_cleanup_and_dry_run(capsys):
    """
    Test synchronization tool (with --clean-to-dir flag).

    Notes
    -----
    Executed in dry-run mode.

    """

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = synchronize(
        owner=owner,
        repository=repository,
        token=TOKEN,
        from_dir=from_dir,
        to_dir=to_dir,
        include_manifest=manifest,
        clean_to_dir=True,
        skip_ci=True,
        random_branch_name=True,
        dry_run=True,
    )

    # Assertions or validations
    assert result is None

    # Check stdout
    captured = capsys.readouterr()[0]

    # Search for the modified files
    assert "src/ansys/api/test/v0/hello_world.py" in captured
    assert "src/ansys/api/test/v0/test.proto" in captured
    assert "src/ansys/tools/repo_sync/__init__.py" in captured
    assert "src/ansys/tools/repo_sync/__main__.py" in captured
    assert "src/ansys/tools/repo_sync/repo_sync.py" in captured


def test_synchronize_with_cleanup_based_on_manifest_and_dry_run(capsys):
    """
    Test synchronization tool (with --clean-to-dir and
    --clean-to-dir-based-on-manifest flags).

    Notes
    -----
    Executed in dry-run mode.

    """

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest_proto_and_init.txt")

    # Call the function
    result = synchronize(
        owner=owner,
        repository=repository,
        token=TOKEN,
        from_dir=from_dir,
        to_dir=to_dir,
        include_manifest=manifest,
        clean_to_dir=True,
        clean_to_dir_based_on_manifest=True,
        skip_ci=True,
        random_branch_name=True,
        dry_run=True,
    )

    # Assertions or validations
    assert result is None

    # Check stdout
    captured = capsys.readouterr()[0]

    # Search for the modified files
    assert "src/ansys/api/test/v0/hello_world.py" not in captured
    assert "src/ansys/api/test/v0/test.proto" in captured
    assert "src/ansys/tools/repo_sync/__init__.py" in captured
    assert "src/ansys/tools/repo_sync/__main__.py" not in captured
    assert "src/ansys/tools/repo_sync/repo_sync.py" not in captured


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_from_cli(tmpdir):
    """Test synchronization tool (without manifest) from CLI."""

    # Define a temp directory and copy assets in it
    shutil.copytree(
        ASSETS_DIRECTORY,
        tmpdir,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest.txt",
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli("ansys", "ansys-tools-repo-sync", completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr("ansys", "ansys-tools-repo-sync", pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo("ansys", "ansys-tools-repo-sync", pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_only_proto_manifest_from_cli(tmpdir):
    """Test synchronization tool (with manifest) from CLI."""

    # Define a temp directory and copy assets in it
    shutil.copytree(
        ASSETS_DIRECTORY,
        tmpdir,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest_only_proto.txt",
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli("ansys", "ansys-tools-repo-sync", completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr("ansys", "ansys-tools-repo-sync", pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo("ansys", "ansys-tools-repo-sync", pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_cleanup_cli(tmpdir):
    """
    Test synchronization tool (with --clean-to-dir flag) from CLI.

    Notes
    -----
    Executed in dry-run mode.

    """

    # Define a temp directory and copy assets in it
    shutil.copytree(
        ASSETS_DIRECTORY,
        tmpdir,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest.txt",
            "--skip-ci",
            "--random-branch-name",
            "--clean-to-dir",
            "--dry-run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Check stdout
    captured = completed_process.stdout.decode()

    # Search for the modified files
    assert "src/ansys/api/test/v0/hello_world.py" in captured
    assert "src/ansys/api/test/v0/test.proto" in captured
    assert "src/ansys/tools/repo_sync/__init__.py" in captured
    assert "src/ansys/tools/repo_sync/__main__.py" in captured
    assert "src/ansys/tools/repo_sync/repo_sync.py" in captured


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_no_sync_cli(tmpdir):
    """Test synchronization tool (with no files needed to be synced) from CLI."""

    # Define a temp directory and copy assets in it
    shutil.copytree(
        ASSETS_DIRECTORY,
        tmpdir,
        dirs_exist_ok=True,
    )

    # Requires installing project
    subprocess.run(
        [
            "pip",
            "install",
            ".",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT_PATH,
    )

    # Call CLI tool
    completed_process = subprocess.run(
        [
            "repo-sync",
            "--token",
            TOKEN,
            "--owner",
            "ansys",
            "--repository",
            "ansys-tools-repo-sync",
            "--from-dir",
            "ansys",
            "--to-dir",
            "src/ansys",
            "--include-manifest",
            "manifest_no_files.txt",
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Check stdout
    captured = completed_process.stdout.decode()

    # Search for the modified files
    assert ">>> No files to sync... Ignoring PR request." in captured
