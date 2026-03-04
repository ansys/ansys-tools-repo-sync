# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Integration tests for repo synchronization behavior."""

import dataclasses
import shutil
import subprocess

import pytest

from ansys.tools.repo_sync.repo_sync import synchronize

from .conftest import (
    ASSETS_DIRECTORY,
    DEFAULT_SYNC_CONFIG,
    ROOT_PATH,
    SKIP_LOCALLY,
    TOKEN,
    check_files_in_pr,
    cleanup_remote_repo,
    get_pr_from_cli,
)


def test_synchronize():
    """Test synchronization tool (without manifest)."""
    cfg = DEFAULT_SYNC_CONFIG

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=cfg.owner,
            repository=cfg.repository,
            token=TOKEN,
            from_dir=cfg.from_dir,
            to_dir=cfg.to_dir,
            include_manifest=cfg.manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert result is not None
        assert "https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(cfg.owner, cfg.repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(cfg.owner, cfg.repository, result)


def test_synchronize_to_existing_pr():
    """Test synchronization tool (when PR already exists)."""
    cfg = DEFAULT_SYNC_CONFIG

    # Call the function
    result = None
    result_pr_already_exists = None
    try:
        result = synchronize(
            owner=cfg.owner,
            repository=cfg.repository,
            token=TOKEN,
            from_dir=cfg.from_dir,
            to_dir=cfg.to_dir,
            include_manifest=cfg.manifest,
            skip_ci=True,
        )

        # Assertions or validations
        assert result is not None
        assert "https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Call the function again - and check that the PR already exists.
        result_pr_already_exists = synchronize(
            owner=cfg.owner,
            repository=cfg.repository,
            token=TOKEN,
            from_dir=cfg.from_dir,
            to_dir=cfg.to_dir,
            include_manifest=cfg.manifest,
            skip_ci=True,
        )

        # Verify the PR is the same
        assert result_pr_already_exists == result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(cfg.owner, cfg.repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(cfg.owner, cfg.repository, result)
        if result_pr_already_exists and result != result_pr_already_exists:
            cleanup_remote_repo(cfg.owner, result_pr_already_exists, result)


def test_synchronize_with_only_proto_manifest():
    """Test synchronization tool (with manifest)."""
    cfg = dataclasses.replace(
        DEFAULT_SYNC_CONFIG, manifest=ASSETS_DIRECTORY / "manifest_only_proto.txt"
    )

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=cfg.owner,
            repository=cfg.repository,
            token=TOKEN,
            from_dir=cfg.from_dir,
            to_dir=cfg.to_dir,
            include_manifest=cfg.manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert result is not None
        assert "https://github.com/ansys/ansys-tools-repo-sync/pull/" in result

        # Check that the proper modified files have been added
        list_of_files = ["src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(cfg.owner, cfg.repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(cfg.owner, cfg.repository, result)


def test_synchronize_no_sync_needed():
    """Test synchronization tool (with manifest referring to non-existing files)."""
    cfg = dataclasses.replace(
        DEFAULT_SYNC_CONFIG, manifest=ASSETS_DIRECTORY / "manifest_no_files.txt"
    )

    # Call the function
    result = None
    try:
        result = synchronize(
            owner=cfg.owner,
            repository=cfg.repository,
            token=TOKEN,
            from_dir=cfg.from_dir,
            to_dir=cfg.to_dir,
            include_manifest=cfg.manifest,
            skip_ci=True,
            random_branch_name=True,
        )

        # Assertions or validations
        assert result is None

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(cfg.owner, cfg.repository, result)


def test_synchronize_with_cleanup_and_dry_run(capsys):
    """
    Test synchronization tool (with --clean-to-dir flag).

    Notes
    -----
    Executed in dry-run mode.

    """
    cfg = DEFAULT_SYNC_CONFIG

    # Call the function
    result = synchronize(
        owner=cfg.owner,
        repository=cfg.repository,
        token=TOKEN,
        from_dir=cfg.from_dir,
        to_dir=cfg.to_dir,
        include_manifest=cfg.manifest,
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
    """Test synchronization tool with manifest-based cleanup.

    Notes
    -----
    Executed in dry-run mode.

    """
    cfg = dataclasses.replace(
        DEFAULT_SYNC_CONFIG, manifest=ASSETS_DIRECTORY / "manifest_proto_and_init.txt"
    )

    # Call the function
    result = synchronize(
        owner=cfg.owner,
        repository=cfg.repository,
        token=TOKEN,
        from_dir=cfg.from_dir,
        to_dir=cfg.to_dir,
        include_manifest=cfg.manifest,
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
    cfg = DEFAULT_SYNC_CONFIG

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
            cfg.owner,
            "--repository",
            cfg.repository,
            "--from-dir",
            cfg.from_dir.name,
            "--to-dir",
            cfg.to_dir,
            "--include-manifest",
            cfg.manifest.name,
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )  # ty:ignore[no-matching-overload]

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli(cfg.owner, cfg.repository, completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr(cfg.owner, cfg.repository, pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo(cfg.owner, cfg.repository, pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_only_proto_manifest_from_cli(tmpdir):
    """Test synchronization tool (with manifest) from CLI."""
    cfg = dataclasses.replace(
        DEFAULT_SYNC_CONFIG, manifest=ASSETS_DIRECTORY / "manifest_only_proto.txt"
    )

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
            cfg.owner,
            "--repository",
            cfg.repository,
            "--from-dir",
            cfg.from_dir.name,
            "--to-dir",
            cfg.to_dir,
            "--include-manifest",
            cfg.manifest.name,
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )  # ty:ignore[no-matching-overload]

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Get the PR associated to the CLI
    pr_url = get_pr_from_cli(cfg.owner, cfg.repository, completed_process.stdout)

    # Check that the proper modified files have been added
    list_of_files = ["src/ansys/api/test/v0/test.proto"]
    assert check_files_in_pr(cfg.owner, cfg.repository, pr_url, list_of_files)

    # Clean up remote repo
    cleanup_remote_repo(cfg.owner, cfg.repository, pr_url)


@pytest.mark.skipif(SKIP_LOCALLY, reason="Only runs on workflow")
def test_synchronize_with_cleanup_cli(tmpdir):
    """
    Test synchronization tool (with --clean-to-dir flag) from CLI.

    Notes
    -----
    Executed in dry-run mode.

    """
    cfg = DEFAULT_SYNC_CONFIG

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
            cfg.owner,
            "--repository",
            cfg.repository,
            "--from-dir",
            cfg.from_dir.name,
            "--to-dir",
            cfg.to_dir,
            "--include-manifest",
            cfg.manifest.name,
            "--skip-ci",
            "--random-branch-name",
            "--clean-to-dir",
            "--dry-run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )  # ty:ignore[no-matching-overload]

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
    cfg = dataclasses.replace(
        DEFAULT_SYNC_CONFIG, manifest=ASSETS_DIRECTORY / "manifest_no_files.txt"
    )

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
            cfg.owner,
            "--repository",
            cfg.repository,
            "--from-dir",
            cfg.from_dir.name,
            "--to-dir",
            cfg.to_dir,
            "--include-manifest",
            cfg.manifest.name,
            "--skip-ci",
            "--random-branch-name",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=tmpdir,
    )  # ty:ignore[no-matching-overload]

    # Check output info
    print(completed_process.returncode)
    print(completed_process.stdout)
    print(completed_process.stderr)

    # Check stdout
    captured = completed_process.stdout.decode()

    # Search for the modified files
    assert ">>> No files to sync... Ignoring PR request." in captured
