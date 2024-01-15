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

"""Tool to copy the content of one repo toward an other.

Run with:

.. code::

    repo-sync \
      --token <token> \
      --owner <organization-name> \
      --repository <repository-name> \
      --from-dir <path-to-dir-containing-files-to-sync> \
      --to-dir <target-dir-for-sync> \
      --include-manifest <path-to-manifest>

"""
import click

from .repo_sync import synchronize as _synchronize


@click.command(short_help="Copy the content of a repository into an other repository.")
@click.option("--owner", "-o", type=str, help="Name of the owner or organization.", required=True)
@click.option("--repository", "-r", type=str, help="Name of the repository.", required=True)
@click.option("--token", "-t", type=str, help="Personal access token.", required=True)
@click.option(
    "--from-dir",
    type=click.Path(file_okay=False, exists=True),
    help="Path to the folder containing the files to copy.",
    required=True,
)
@click.option(
    "--to-dir",
    type=click.Path(file_okay=False),
    help="Path of the folder that will contain the files (w.r.t. the root of the repository).",
    required=True,
)
@click.option(
    "--include-manifest",
    "-m",
    type=click.Path(dir_okay=False, exists=True),
    help="Manifest to mention accepted extension files.",
    required=True,
)
@click.option("--branch_checked_out", "-b", type=str, help="Branch to check out.", default="main")
@click.option(
    "--clean-to-dir",
    is_flag=True,
    default=False,
    help="Clean the folder defined in --to-dir before synchronizing.",
)
@click.option(
    "--clean-to-dir-based-on-manifest",
    is_flag=True,
    default=False,
    help=(
        "Deletion of target directory is performed based on manifest file"
        " (i.e. only those files matching the extensions on it are deleted)."
        " Only has an effect if --clean-to-dir is passed."
    ),
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="Simulate the behavior of the synchronization without performing it.",
)
@click.option(
    "--skip-ci",
    is_flag=True,
    default=False,
    help="Adds a ``[skip ci]`` prefix to the commit message or not.",
)
@click.option(
    "--random-branch-name",
    is_flag=True,
    default=False,
    help="Generates a random branch name instead of the typical ``sync/file-sync``. Used for testing purposes mainly.",
)
def synchronize(
    owner,
    repository,
    token,
    from_dir,
    to_dir,
    include_manifest,
    branch_checked_out,
    clean_to_dir,
    clean_to_dir_based_on_manifest,
    dry_run,
    skip_ci,
    random_branch_name,
):
    """CLI command to execute the repository synchronization."""
    _synchronize(
        owner=owner,
        repository=repository,
        token=token,
        from_dir=from_dir,
        to_dir=to_dir,
        clean_to_dir=clean_to_dir,
        clean_to_dir_based_on_manifest=clean_to_dir_based_on_manifest,
        include_manifest=include_manifest,
        branch_checked_out=branch_checked_out,
        dry_run=dry_run,
        skip_ci=skip_ci,
        random_branch_name=random_branch_name,
    )


if __name__ == "__main__":
    synchronize()
